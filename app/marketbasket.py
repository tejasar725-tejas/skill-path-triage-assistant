"""Frequent skill-pattern mining (self-contained Apriori-style implementation).

Each employee sequence is treated as a transaction for frequent itemsets; adjacent
chronological pairs are additionally mined as directional transition rules.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations


def mine_frequent_itemsets(transactions: list[list[str]], min_support: float = 0.15,
                           max_size: int = 3) -> list[dict]:
    if not 0 < min_support <= 1:
        raise ValueError("min_support must be in (0, 1].")
    baskets = [set(t) for t in transactions if t]
    if not baskets:
        return []
    counts = Counter()
    universe = sorted(set().union(*baskets))
    for size in range(1, min(max_size, len(universe)) + 1):
        for combo in combinations(universe, size):
            count = sum(set(combo).issubset(b) for b in baskets)
            support = count / len(baskets)
            if support >= min_support:
                counts[combo] = support
    return [{"items": list(items), "support": support, "count": round(support * len(baskets))}
            for items, support in sorted(counts.items(), key=lambda x: (-x[1], len(x[0]), x[0]))]


def mine_transition_rules(sequences: list[list[str]], min_support: float = 0.05,
                          min_confidence: float = 0.2) -> list[dict]:
    pair_counts, source_counts = Counter(), Counter()
    total = 0
    for seq in sequences:
        for a, b in zip(seq, seq[1:]):
            pair_counts[(a, b)] += 1
            source_counts[a] += 1
            total += 1
    rules = []
    for (a, b), count in pair_counts.items():
        support = count / max(total, 1)
        confidence = count / source_counts[a]
        if support >= min_support and confidence >= min_confidence:
            rules.append({"from": a, "to": b, "count": count,
                          "support": support, "confidence": confidence})
    return sorted(rules, key=lambda r: (-r["confidence"], -r["support"], r["to"]))
