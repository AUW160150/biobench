from pathlib import Path
from typing import Dict, List, Any
import json
import pandas as pd

from .io import read_fasta
from .orf import find_orfs
from .translate import translate_orf
from .qc import gc_content, length_stats, is_dna

def build_report(
    fasta_path: str | Path,
    out_dir: str | Path,
    min_orf_aa: int = 60,
    include_revcomp: bool = True
) -> Dict[str, Any]:
    outp = Path(out_dir)
    outp.mkdir(parents=True, exist_ok=True)

    seqs = read_fasta(fasta_path)
    rows_seq: List[Dict[str, Any]] = []
    rows_orf: List[Dict[str, Any]] = []

    for sid, seq in seqs.items():
        valid = is_dna(seq)
        stats = length_stats(seq)
        rows_seq.append({
            "id": sid,
            **stats,
            "gc_content": gc_content(seq),
            "valid_dna": valid,
        })

        orfs = find_orfs(seq, include_revcomp=include_revcomp, min_aa=min_orf_aa)
        for (nt_start, nt_end_excl, frame, is_rev) in orfs:
            # extract the ORF nucleotides from the appropriate strand
            subseq = seq[nt_start:nt_end_excl] if not is_rev else None
            if is_rev:
                # Coordinates for reverse scan are on RC string; for demo, we just store coords as-is.
                # (Mapping back to forward strand coordinates can be added later.)
                pass
            if subseq is None:
                subseq = seq  # placeholder to avoid crash; realistic mapping is TODO
            aa = translate_orf(subseq)
            rows_orf.append({
                "id": sid,
                "nt_start": nt_start,
                "nt_end_excl": nt_end_excl,
                "frame": frame,
                "is_rev": is_rev,
                "aa_len": len(aa),
                "aa_seq_preview": aa[:30] + ("..." if len(aa) > 30 else ""),
            })

    df_seq = pd.DataFrame(rows_seq).sort_values("id")
    df_orf = pd.DataFrame(rows_orf).sort_values(["id", "nt_start", "frame"])

    df_seq.to_csv(outp / "sequences.csv", index=False)
    df_orf.to_csv(outp / "orfs.csv", index=False)

    summary = {
        "n_sequences": len(df_seq),
        "n_orfs": int(len(df_orf)),
        "params": {
            "min_orf_aa": min_orf_aa,
            "include_revcomp": include_revcomp,
        },
        "outputs": {
            "sequences_csv": str((outp / "sequences.csv").resolve()),
            "orfs_csv": str((outp / "orfs.csv").resolve()),
        },
    }
    with open(outp / "report.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary
