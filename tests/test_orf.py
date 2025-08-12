from biobench.orf import find_orfs

def test_find_orfs_basic():
    # ATG at index 3, stop TAA ends at index 18 (end-exclusive), frame +0
    seq = "AAAATGAAAGGGTTTTAAACC"
    orfs = find_orfs(seq, include_revcomp=False, min_aa=2)
    assert any((s, e, f, r) == (3, 18, "+0", False) for (s, e, f, r) in orfs)
