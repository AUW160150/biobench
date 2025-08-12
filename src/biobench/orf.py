from typing import List, Tuple

STOP_CODONS = {"TAA", "TAG", "TGA"}
START_CODON = "ATG"

def reverse_complement(seq: str) -> str:
    comp = str.maketrans("ACGTN", "TGCAN")
    return seq.upper().translate(comp)[::-1]

def _codons(seq: str, frame: int) -> List[str]:
    end = len(seq) - ((len(seq) - frame) % 3)
    return [seq[i:i+3] for i in range(frame, end, 3)]

def find_orfs(
    seq: str,
    include_revcomp: bool = False,
    min_aa: int = 0
) -> List[Tuple[int, int, str, bool]]:
    """
    Returns list of ORFs: (nt_start, nt_end_excl, frame_strand, is_rev)
    frame_strand is one of: '+0', '+1', '+2', '-0', '-1', '-2'
    Coordinates are 0-based on the strand scanned (RC has its own coords).
    """
    s = seq.upper().replace("U", "T")
    orfs: List[Tuple[int, int, str, bool]] = []

    def scan(ss: str, sign: str) -> List[Tuple[int, int, str, bool]]:
        found: List[Tuple[int, int, str, bool]] = []
        for frame in range(3):
            cods = _codons(ss, frame)
            start_idx = None
            for i, cod in enumerate(cods):
                if start_idx is None:
                    if cod == START_CODON:
                        start_idx = i
                else:
                    if cod in STOP_CODONS:
                        nt_start = frame + start_idx * 3
                        nt_end_excl = frame + (i + 1) * 3
                        aa_len = (nt_end_excl - nt_start) // 3
                        if aa_len >= min_aa:
                            found.append((nt_start, nt_end_excl, f"{sign}{frame}", sign == "-"))
                        start_idx = None
        return found

    orfs.extend(scan(s, "+"))
    if include_revcomp:
        rc = reverse_complement(s)
        orfs.extend(scan(rc, "-"))
    return orfs
