from app.cli import main as cli_main
from app.core import milestone_1, milestone_2, milestone_3, milestone_4, milestone_5


def test_milestone_1():
    seqs = milestone_1()
    assert len(seqs) >= 8
    assert all(len(v) >= 2 for v in seqs.values())


def test_milestone_2():
    seqs = milestone_1()
    patterns = milestone_2(seqs, min_support=0.2, min_confidence=0.4)
    assert len(patterns) > 0


def test_milestone_3():
    seqs = milestone_1()
    lm = milestone_3(seqs, seed=42)
    preds = lm.predict_next(["role:junior_analyst", "skill:sql"], top_n=2)
    assert len(preds) > 0


def test_milestone_4():
    seqs = milestone_1()
    metrics = milestone_4(seqs, top_n=3, seed=42)
    assert metrics["test_count"] > 0
    assert float(metrics["lm_top_n_acc"]) >= float(metrics["baseline_top1_acc"])


def test_milestone_5(capsys):
    suggestions = milestone_5(["skill:python"], top_n=2)
    assert len(suggestions) <= 2
    cli_main(["suggest", "role:junior_analyst", "skill:sql", "--top-n", "2"])
    assert "Current profile:" in capsys.readouterr().out
