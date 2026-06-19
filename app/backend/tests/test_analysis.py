from pathlib import Path
from tuneez.core.blackbox import load_blackbox
from tuneez.core.cli_parser import parse_cli_dump
from tuneez.core.models import BuildProfile
from tuneez.core.recommend import analyze

ROOT = Path(__file__).resolve().parents[3]

def test_sample_analysis():
    df = load_blackbox(str(ROOT / "samples" / "sample_blackbox.csv"))
    cfg = parse_cli_dump((ROOT / "samples" / "sample_cli.txt").read_text())
    report = analyze(df, cfg, BuildProfile(gyro="BMI270", symptoms=["hot motors"]))
    assert "save" in report.cli
    assert len(report.findings) >= 1
    assert report.scores["tracking"] >= 0
