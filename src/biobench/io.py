
from pathlib import Path
from typing import Dict
from Bio import SeqIO

def read_fasta(path: str | Path) -> Dict[str, str]:
    records = SeqIO.parse(str(path), "fasta")
    return {r.id: str(r.seq).upper() for r in records}

def read_fastq(path: str | Path) -> Dict[str, str]:
    records = SeqIO.parse(str(path), "fastq")
    return {r.id: str(r.seq).upper() for r in records}
