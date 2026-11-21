from app.core import SkillNGramLM, prepare_sequences, evaluate_model, build_report
from app.storage import load_sequences
from app.marketbasket import mine_frequent_itemsets, mine_transition_rules


def test_load_and_prepare_sequences():
    rows = load_sequences()
    seqs = prepare_sequences(rows)
    assert len(seqs) == len(rows)
    assert seqs[0][:2] == ["Excel", "SQL"]


def test_ngram_model_predicts_known_next_skill():
    model = SkillNGramLM(n=2, alpha=0.01).fit([["Python", "Pandas"], ["Python", "Pandas"], ["SQL", "Excel"]])
    assert model.predict(["Python"], 1)[0]["skill"] == "Pandas"


def test_frequent_itemset_and_transition_mining():
    itemsets = mine_frequent_itemsets([["A", "B"], ["A", "B"], ["A", "C"]], min_support=0.5)
    assert any(x["items"] == ["A", "B"] for x in itemsets)
    rules = mine_transition_rules([["A", "B"], ["A", "B"], ["A", "C"]], min_support=0.1, min_confidence=0.2)
    assert any(x["from"] == "A" and x["to"] == "B" for x in rules)


def test_report_and_evaluation():
    rows = load_sequences()
    report = build_report(rows)
    assert report["employees"] == len(rows)
    metrics = evaluate_model(rows)
    assert metrics["examples"] > 0
    assert 0 <= metrics["top3_accuracy"] <= 1
