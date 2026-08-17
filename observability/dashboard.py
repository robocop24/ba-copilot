import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from observability.log_analyzer import LogAnalyzer


def main():
    analyzer = LogAnalyzer()

    print("\n=== BA COPILOT DASHBOARD ===\n")

    print("Counters (derived from logs)")
    print("-" * 30)
    print(f"workflows:     {analyzer.workflow_count()}")
    print(f"llm_calls:     {analyzer.llm_call_count()}")
    print(f"mcp_calls:     {analyzer.mcp_call_count()}")
    print(f"cache_hits:    {analyzer.cache_hit_count()}")
    print(f"cache_misses:  {analyzer.cache_miss_count()}")
    print(f"rag_queries:   {analyzer.rag_query_count()}")
    print(f"errors:        {analyzer.error_count()}")

    print("\nComponent Latency")
    print("-" * 30)
    for component, stats in analyzer.component_latency_stats().items():
        print(f"{component}: count={stats['count']} avg={stats['avg_ms']}ms "
              f"min={stats['min_ms']}ms max={stats['max_ms']}ms")

    print("\nComponent Log Counts")
    print("-" * 30)
    for component, count in analyzer.component_log_counts().items():
        print(f"{component}: {count}")

    slowest = analyzer.slowest_component()
    if slowest:
        name, stats = slowest
        print(f"\nSlowest component: {name} (avg {stats['avg_ms']}ms)")


if __name__ == "__main__":
    main()
