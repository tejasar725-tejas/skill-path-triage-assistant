from __future__ import annotations

import csv
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

try:
    import thilimarketbasket as tmb  # type: ignore
except Exception:
    tmb = None


@dataclass
class SkillEvent:
    employee_id: str
    step: int
    event_date: str
    skill_or_role: str


@dataclass
class TransitionPattern:
    antecedent: str
    consequent: str
    count: int
    support: float
    confidence: float


@dataclass
class NextStepLM:
    unigram_counts: Counter
    bigram_counts: Dict[str, Counter]
    total_tokens: int
    vocab: List[str]

    def predict_next(
        self,
        current_items: Sequence[str],
        top_n: int = 3,
        exclude_seen: bool = True,
    ) -> List[Tuple[str, float]]:
        seen = {item.strip() for item in current_items if item and item.strip()}
        if not seen:
            return []

        scores: Counter = Counter()
        for item in seen:
            next_counter = self.bigram_counts.get(item)
            if next_counter:
                total_after = sum(next_counter.values())
                for nxt, cnt in next_counter.items():
                    if exclude_seen and nxt in seen:
                        continue
                    scores[nxt] += cnt / max(total_after, 1)

        if not scores:
            for tok, cnt in self.unigram_counts.most_common():
                if exclude_seen and tok in seen:
                    continue
                scores[tok] += cnt / max(self.total_tokens, 1)

        total_score = sum(scores.values())
        if total_score <= 0:
            return []
        return [(tok, round(val / total_score, 4)) for tok, val in scores.most_common(top_n)]


def set_seed(seed: int = 42) -> None:
    random.seed(seed)


def default_data_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "skill_sequences.csv"


def milestone_1(csv_path: str | Path | None = None) -> Dict[str, List[str]]:
    path = Path(csv_path) if csv_path else default_data_path()
    events_by_emp: Dict[str, List[SkillEvent]] = defaultdict(list)
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            emp = (row.get("employee_id") or "").strip()
            step_raw = (row.get("step") or "0").strip()
            dt = (row.get("event_date") or "").strip()
            item = (row.get("skill_or_role") or "").strip()
            if emp and item:
                step_num = int(step_raw) if step_raw.isdigit() else 0
                events_by_emp[emp].append(SkillEvent(emp, step_num, dt, item))
    sequences: Dict[str, List[str]] = {}
    for emp, evs in sorted(events_by_emp.items()):
        evs_sorted = sorted(evs, key=lambda e: (e.step, e.event_date))
        sequences[emp] = [e.skill_or_role for e in evs_sorted]
    return sequences


def milestone_2(
    sequences: Dict[str, List[str]],
    min_support: float = 0.2,
    min_confidence: float = 0.5,
) -> List[TransitionPattern]:
    seq_list = [seq for seq in sequences.values() if len(seq) >= 2]
    if not seq_list:
        return []
    _ = tmb
    pair_counts: Counter = Counter()
    num_seqs = len(seq_list)
    for seq in seq_list:
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i + 1]
            if a != b:
                pair_counts[(a, b)] += 1
    patterns: List[TransitionPattern] = []
    for (a, b), cnt in pair_counts.most_common():
        support = cnt / num_seqs
        ant_total = sum(c for (x, _), c in pair_counts.items() if x == a)
        confidence = cnt / max(ant_total, 1)
        if support >= min_support and confidence >= min_confidence:
            patterns.append(
                TransitionPattern(a, b, cnt, round(support, 4), round(confidence, 4))
            )
    return patterns


def milestone_3(sequences: Dict[str, List[str]], seed: int = 42) -> NextStepLM:
    set_seed(seed)
    unigram: Counter = Counter()
    bigrams: Dict[str, Counter] = defaultdict(Counter)
    vocab_set = set()
    for seq in sequences.values():
        for idx, tok in enumerate(seq):
            unigram[tok] += 1
            vocab_set.add(tok)
            if idx + 1 < len(seq):
                bigrams[tok][seq[idx + 1]] += 1
    return NextStepLM(unigram, dict(bigrams), sum(unigram.values()), sorted(vocab_set))


def milestone_4(
    sequences: Dict[str, List[str]],
    top_n: int = 3,
    seed: int = 42,
) -> Dict[str, object]:
    set_seed(seed)
    train_seqs: Dict[str, List[str]] = {}
    test_pairs: List[Tuple[List[str], str]] = []
    for emp, seq in sorted(sequences.items()):
        if len(seq) >= 3:
            train_seqs[emp] = seq[:-1]
            test_pairs.append((seq[:-1], seq[-1]))
        elif len(seq) == 2:
            train_seqs[emp] = seq
            test_pairs.append(([seq[0]], seq[1]))
    if not test_pairs:
        return {"test_count": 0, "baseline_top1_acc": 0.0, "lm_top1_acc": 0.0, "lm_top_n_acc": 0.0, "top_n": top_n}

    lm = milestone_3(train_seqs, seed=seed)
    majority = lm.unigram_counts.most_common(1)[0][0] if lm.unigram_counts else ""
    base_ok = top1_ok = topn_ok = 0
    for hist, target in test_pairs:
        if majority == target:
            base_ok += 1
        preds = [p[0] for p in lm.predict_next(hist, top_n=top_n, exclude_seen=False)]
        if preds:
            if preds[0] == target:
                top1_ok += 1
            if target in preds:
                topn_ok += 1
    n = len(test_pairs)
    return {
        "test_count": n,
        "baseline_top1_acc": round(base_ok / n, 4),
        "lm_top1_acc": round(top1_ok / n, 4),
        "lm_top_n_acc": round(topn_ok / n, 4),
        "top_n": top_n,
    }


def milestone_5(
    current_items: Sequence[str],
    top_n: int = 3,
    csv_path: str | Path | None = None,
    seed: int = 42,
) -> List[Tuple[str, float]]:
    sequences = milestone_1(csv_path)
    lm = milestone_3(sequences, seed=seed)
    return lm.predict_next(current_items, top_n=top_n, exclude_seen=True)


def write_evaluation_report(
    output_path: str | Path,
    metrics: Dict[str, object],
    patterns: List[TransitionPattern],
    sample_suggestions: Dict[str, List[Tuple[str, float]]],
) -> Path:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Skill Path Evaluation & Analysis Report",
        "",
        "## Model vs. Baseline Evaluation",
        "",
        f"- **Evaluated Sequences:** `{metrics['test_count']}`",
        f"- **Majority Baseline Top-1 Accuracy:** `{float(metrics['baseline_top1_acc']):.2%}`",
        f"- **Next-Step LM Top-1 Accuracy:** `{float(metrics['lm_top1_acc']):.2%}`",
        f"- **Next-Step LM Top-{metrics['top_n']} Accuracy:** `{float(metrics['lm_top_n_acc']):.2%}`",
        "",
        "## Top Discovered Skill/Role Transitions",
        "",
        "| Antecedent | Consequent | Count | Support | Confidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    for p in patterns[:10]:
        lines.append(f"| `{p.antecedent}` | `{p.consequent}` | {p.count} | {p.support:.2f} | {p.confidence:.2f} |")
    lines.extend(["", "## Sample CLI Next-Step Suggestions", ""])
    for query, preds in sample_suggestions.items():
        formatted = ", ".join(f"`{name}` ({score:.1%})" for name, score in preds) or "None"
        lines.append(f"- **Input:** `{query}` -> {formatted}")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8-sig")
    return out


def generate_default_report(report_path: str | Path = "reports/evaluation_report.md") -> Path:
    sequences = milestone_1()
    patterns = milestone_2(sequences, min_support=0.2, min_confidence=0.4)
    metrics = milestone_4(sequences, top_n=3, seed=42)
    sample_queries = [
        "role:junior_analyst,skill:sql",
        "skill:python",
        "role:data_analyst,skill:machine_learning",
    ]
    suggestions = {
        q: milestone_5([x.strip() for x in q.split(",")], top_n=3)
        for q in sample_queries
    }
    return write_evaluation_report(report_path, metrics, patterns, suggestions)


if __name__ == "__main__":
    out_file = generate_default_report()
    print(f"Wrote report to {out_file}")

