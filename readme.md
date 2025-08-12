# BioBench – AI-Reviewed Genomics Mini-Pipeline

Reads FASTA, finds ORFs, translates, computes QC, and writes CSV + JSON summary.
Designed to showcase **CodeRabbit** (IDE + PR reviews) and **Goose** subagents for automation.

## Quickstart
```bash
# in PowerShell, after activating venv
py -m pip install -r requirements.txt

# put demo.fasta in data/
py -m biobench.cli --in data/demo.fasta --out out --min-orf-aa 2
