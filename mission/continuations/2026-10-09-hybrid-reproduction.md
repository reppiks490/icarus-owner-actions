# Portable current hybrid audit

Download [the source-pinned reproduction packet](2026-10-09-hybrid-reproduction.tar.gz) and extract it into a scratch directory. Its README supplies an explicit-input, scratch-output command tested on Python 3.12. All supplied records derive from already-public pinned Git objects; no provider data or private storage references are included.

Archive SHA-256: `a7956f06df1550b35017d733a981ea33f79e640fac2c7a7a4f6956c673c26131`. Archive bytes: 241801; members: 505. Gzip integrity and every archived member equality against the previously CRC-verified ZIP were checked. `SHA256SUMS` records packet member digests, and the runner also rehashes Git blob bytes and tree objects.

The [canonical audit report](2026-10-09-hybrid-reconciliation.json) preserves its original producer script hash. The packet contains a separately generated portable report, whose only report difference is the portable runner hash. Counts, source identity, main observation clock and original-result evidence are identical. Neither report changes historical source records or grants completion credit. This new audit packet is separate from the eleven original provider Actions ZIPs, which remain unmaterialized.
