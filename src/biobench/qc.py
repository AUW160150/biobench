from collections import Counter
from typing import Dict, Tuple

def is_dna(seq: str) -> bool:
    s = seq.upper()
    return all(c in "ACGTN" for c in s)

def gc_content(seq: str) -> float:
    s = seq.upper()
    total = sum(1 for c in s if c in "ACGT")
    if total == 0:
        return 0.0
    gc = sum(1 for c in s if c in "GC")
    return gc / total

def length_stats(seq: str) -> Dict[str, int | float]:
    n = len(seq)
    counts = Counter(seq.upper())
    return {
        "length_nt": n,
        "count_A": counts.get("A", 0),
        "count_C": counts.get("C", 0),
        "count_G": counts.get("G", 0),
        "count_T": counts.get("T", 0),
        "count_N": counts.get("N", 0),
    }
