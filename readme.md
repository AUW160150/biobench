BioBench — AI-Reviewed Genomics Mini-Pipeline
What It Does
BioBench reads a FASTA file, finds ORFs (Open Reading Frames) on both strands, translates them to amino acids, computes QC metrics (GC%, base counts), and writes tidy outputs in multiple formats: CSV, JSON, and human-friendly HTML/Markdown summaries.

Why It Matters
Small bioinformatics pipelines often fail silently on edge cases (empty inputs, reverse-strand mapping, sequence normalization).
BioBench demonstrates how AI-driven code review and agentic automation improve correctness, reproducibility, and developer experience.

🧠 AI Tools Used
CodeRabbit (IDE + PR Reviews)
Caught and helped fix correctness issues:

Empty FASTA handling in report.py (now emits valid empty artifacts + summary)

Consistent sequence normalization (uppercase + U→T) across translate.py / orf.py

CLI input validation (clear error + non-zero exit on missing file)

Reverse-strand coordinate mapping bug (now fixed + covered by test)
📄 See: WHAT_CODERABBIT_CAUGHT.md

Goose (Subagents)
Summarizer agent reads out/report.json + out/orfs.csv and generates out/summary.md (≤150 words).

Runner+Summarizer flow documented in GOOSE.md.
(Windows tool friction noted; chat-based Summarizer path still demonstrates agentic value.)

⚡ How to Run
(Windows, PowerShell, venv active)

powershell
Copy
Edit
$env:PYTHONPATH="src"
py -m pytest
py -m biobench.cli --in data/demo.fasta --out out --min-orf-aa 2 --include-revcomp
py -m biobench.summarizer --out out
py -m biobench.html_report --out out
📂 Outputs
out/sequences.csv — per-sequence stats

out/orfs.csv — ORFs with strand, frame, forward-mapped coords

out/report.json — machine-readable summary

out/report.html — judge-friendly HTML overview

out/summary.md — Goose Summarizer output

🔗 Repo
https://github.com/AUW160150/biobench
