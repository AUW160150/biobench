import argparse
from .report import build_report

def main():
    ap = argparse.ArgumentParser(description="BioBench mini genomics pipeline")
    ap.add_argument("--in", dest="fin", required=True, help="Input FASTA file")
    ap.add_argument("--out", dest="out_dir", required=True, help="Output directory")
    ap.add_argument("--min-orf-aa", type=int, default=60)
    ap.add_argument("--include-revcomp", action="store_true", default=False)
    args = ap.parse_args()

    print(f"[INFO] Running pipeline on: {args.fin}")
    summary = build_report(
        fasta_path=args.fin,
        out_dir=args.out_dir,
        min_orf_aa=args.min_orf_aa,
        include_revcomp=args.include_revcomp,
    )
    print("[INFO] Report written:")
    for k, v in summary["outputs"].items():
        print(f"  {k}: {v}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
