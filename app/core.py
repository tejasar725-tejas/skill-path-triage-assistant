"""Sequence preparation, n-gram next-skill LM, evaluation and reporting."""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
import json
from .storage import load_sequences
from .marketbasket import mine_frequent_itemsets, mine_transition_rules

START = "<START>"


def prepare_sequences(records: list[dict]) -> list[list[str]]:
    """Convert each employee's ordered skills into a model sequence."""
    return [[str(skill).strip() for skill in row["skills"] if str(skill).strip()]
            for row in records]


class SkillNGramLM:
    """Smoothed n-gram language model for next-skill prediction."""
    def __init__(self, n: int = 2, alpha: float = 0.5):
        if n < 1 or alpha <= 0:
            raise ValueError("n must be >= 1 and alpha must be > 0")
        self.n, self.alpha = n, alpha
        self.context_counts = defaultdict(Counter)
        self.unigram_counts = Counter()
        self.vocab: set[str] = set()

    def fit(self, sequences: list[list[str]]) -> "SkillNGramLM":
        for seq in sequences:
            tokens = [START] * (self.n - 1) + list(seq) + ["<END>"]
            for i, token in enumerate(tokens):
                self.unigram_counts[token] += 1
                self.vocab.add(token)
                if self.n > 1:
                    context = tuple(tokens[max(0, i-self.n+1):i])
                    context = (START,) * (self.n - 1 - len(context)) + context
                else:
                    context = tuple()
                self.context_counts[context][token] += 1
        return self

    def predict(self, skills: list[str], top_n: int = 5) -> list[dict]:
        if top_n < 1:
            raise ValueError("top_n must be >= 1")
        context = tuple((([START] * max(0, self.n - 1 - len(skills))) + skills)[-(self.n-1):]) if self.n > 1 else tuple()
        counts = self.context_counts.get(context, Counter())
        candidates = sorted(self.vocab - {START, "<END>"})
        if not candidates:
            return []
        denom = sum(counts.values()) + self.alpha * len(self.vocab)
        probs = {word: (counts.get(word, 0) + self.alpha) / max(denom, 1e-12)
                 for word in candidates}
        # Normalize only across displayable skill candidates.
        norm = sum(probs.values()) or 1.0
        ranked = sorted(((word, value / norm) for word, value in probs.items()),
                        key=lambda x: (-x[1], x[0]))
        return [{"skill": word, "likelihood": score} for word, score in ranked[:top_n]]


def train_model(data_path=None, n: int = 2, alpha: float = 0.5) -> SkillNGramLM:
    return SkillNGramLM(n=n, alpha=alpha).fit(prepare_sequences(load_sequences(data_path)))


def evaluate_model(records: list[dict], n: int = 2, alpha: float = 0.5) -> dict:
    """Chronological holdout: predict each employee's final skill from prior skills."""
    train_sequences, tests = [], []
    for row in records:
        skills = row["skills"]
        if len(skills) >= 3:
            train_sequences.append(skills[:-1])
            tests.append((skills[:-1], skills[-1]))
    if not tests:
        return {"examples": 0, "top1_accuracy": 0.0, "top3_accuracy": 0.0}
    model = SkillNGramLM(n=n, alpha=alpha).fit(train_sequences)
    top1 = top3 = 0
    for prefix, target in tests:
        preds = model.predict(prefix, top_n=3)
        names = [p["skill"] for p in preds]
        top1 += bool(names and names[0] == target)
        top3 += target in names
    return {"examples": len(tests), "top1_accuracy": top1 / len(tests),
            "top3_accuracy": top3 / len(tests)}


def build_report(records: list[dict]) -> dict:
    sequences = prepare_sequences(records)
    transactions = [list(dict.fromkeys(seq)) for seq in sequences]
    return {
        "employees": len(records),
        "frequent_itemsets": mine_frequent_itemsets(transactions, min_support=0.15),
        "transition_rules": mine_transition_rules(sequences, min_support=0.02, min_confidence=0.15),
        "skill_frequency": dict(Counter(skill for seq in sequences for skill in seq).most_common()),
    }


def find_skill_gaps(records: list[dict], top_n: int = 10) -> list[dict]:
    counts = Counter(skill for row in records for skill in row["skills"])
    total = len(records)
    return [{"skill": skill, "employee_count": count,
             "coverage": count / total if total else 0.0}
            for skill, count in sorted(counts.items(), key=lambda x: (x[1], x[0]))[:top_n]]


def save_report(report: dict, output: str | Path = "outputs/skill_path_report.json") -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path
