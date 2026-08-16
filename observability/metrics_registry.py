from pathlib import Path

from .metrics import Metrics

METRICS_DIR = Path(__file__).resolve().parent / "metrics"

metrics = Metrics()


def save_metrics(file_name: str) -> None:
    metrics.save_snapshot(str(METRICS_DIR / file_name))