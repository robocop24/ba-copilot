# Challenge 11: Cost Visibility — Placeholder Pricing Under-reported Cost by 5–11×

## The Problem

The dashboard showed ~`$0.003` per workflow run, yet `$2` of DeepSeek credit vanished
over 4 days of development. Either the runs were absurdly numerous, or the dashboard's
cost number was wrong. It was the latter.

## Root Cause: made-up price constants

`observability/log_analyzer.py` estimated cost with placeholder constants:

```python
INPUT_COST_PER_1M = 0.14
OUTPUT_COST_PER_1M = 0.28
```

These were guesses. The **real** DeepSeek V4 Pro pricing (from the official pricing
page) is far higher:

| | Off-peak | Peak |
|---|---|---|
| Input (cache miss) | $0.66 / 1M | $1.32 / 1M |
| Input (cache hit) | $0.022 / 1M | $0.044 / 1M |
| **Output** | **$1.98 / 1M** | **$3.96 / 1M** |

So output was **7×** the placeholder and input **~4.7×**. Peak hours (01:00–04:00 &
06:00–10:00 UTC) double it again.

## The real math (one run: 13,744 tokens)

| | input (10,135) | output (3,609) | total |
|---|---|---|---|
| Placeholder | $0.0014 | $0.0010 | **$0.0024** |
| Real, off-peak | $0.0067 | $0.0071 | **$0.0138** |
| Real, peak | $0.0134 | $0.0143 | **$0.0277** |

The dashboard under-reported by **5.7× (off-peak) to 11.4× (peak)**.

## Where the $2 went

$$ \frac{\$2}{\$0.014\text{–}0.028 \text{ / run}} = 72\text{–}143 \text{ runs} $$

Over 4 days of active iteration (each debug cycle = one full run), that is entirely
plausible. It was never "one expensive run" — it was many runs at a price the dashboard
wasn't showing.

The token drivers *within* each run (from the log-derived breakdown):

| Node | tokens | note |
|---|---|---|
| REFINEMENT | 3,047 | rejection loop (every `n` at approval re-runs planner+review) |
| REVIEW (2nd) | 2,515 | full state |
| ESTIMATION (ReAct) | 1,567 | multiple internal LLM calls |
| ANALYZER (ReAct) | 1,535 | + RAG retrieval |
| ACCEPTANCE | 1,509 | largest single output (1,120 tokens) |
| REVIEW (1st) | 1,166 | **wasted** — ran with `"N/A"` inputs (see Challenge 10) |

## The Fix

Replace the placeholder constants with the real rates (off-peak cache-miss as the
baseline), and keep cost **log-derived** — every LLM call already logs
`prompt_tokens`/`completion_tokens`/`total_tokens`:

```python
# log_analyzer.py
INPUT_COST_PER_1M = 0.66    # input, cache miss, off-peak
OUTPUT_COST_PER_1M = 1.98   # output, off-peak
```

Now the dashboard's `workflow_cost = prompt_tokens/1M × 0.66 + completion_tokens/1M × 1.98`
reflects reality instead of fiction.

## Caveats

- **Peak vs off-peak** — the constants use off-peak; peak hours cost 2×.
- **Cache hits** — repeated identical prefixes cost ~30× less on input ($0.022/1M);
  the dashboard doesn't yet split cache hit/miss.
- **Thinking mode** — DeepSeek V4 Pro defaults to thinking mode; reasoning tokens are
  billed as *output*. Our observed `completion_tokens` were small, so the model was in
  non-thinking mode, but a model switch could silently multiply output cost.

## Key Takeaway

> A cost dashboard with made-up constants is worse than no dashboard — it gives false
> confidence while money burns. Verify prices against the provider's official page, and
> derive cost from logged token counts so the number is always computed, never hardcoded.
