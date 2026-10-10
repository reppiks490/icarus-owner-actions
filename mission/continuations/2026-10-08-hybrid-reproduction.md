# Reproducing the pinned hybrid reconciliation

The [recorded report](2026-10-08-hybrid-reconciliation.json) uses Engine source `b9e6013aa578c1638ed5fb023563776ff72d5888` and the exact [tree manifest](2026-10-08-hybrid-tree.json), whose SHA-256 is `91c6b2c9b09fa6975d01c8eddfe2c98ca98ba421ae5c38179913af25195ec85c`. The offline auditor rehashes every request/result blob and checks its supplied tree byte size before parsing it. Four mutable `latest.json` mirrors are checked against their immutable targets and excluded from the denominator.

The recorded audit also executes the pinned Engine `result_valid` implementation against all 372 immutable request identities. Its source path is `tools/hybrid_loop_bridge.py`, Git blob SHA `f4ecdfdd0c8448245b8b7dadb43a1ccec7b5462f`, SHA-256 `c6239759bf66d4173940212d6ad9e54d9e7f48f25dd518467ad2938459b9cbe1`, and size 15,575 bytes. It agrees with the auditor: five strictly valid matching results and 367 unresolved requests.

The following optional review commands run locally after the pinned commit's objects are available in an Engine checkout. They do not fetch objects, call providers, modify the checkout, change automations or publish request payloads. Keep generated inputs outside this mission repository. Replace the two filesystem placeholders with a local checkout and a new scratch directory. The scratch directory is created privately and exclusively on POSIX; Windows ACL privacy requires separate verification.

```sh
export ICARUS_AUDIT_ENGINE_REPO=/absolute/path/to/Icarus-engine
export ICARUS_AUDIT_SCRATCH=/absolute/path/to/private/audit-scratch
python - <<'PY'
import json
import os
from pathlib import Path
import subprocess

repo = Path(os.environ['ICARUS_AUDIT_ENGINE_REPO'])
scratch = Path(os.environ['ICARUS_AUDIT_SCRATCH'])
scratch.mkdir(mode=0o700, parents=True, exist_ok=False)
blobs = scratch / 'blobs'
blobs.mkdir(mode=0o700)
tree = json.loads(Path('mission/continuations/2026-10-08-hybrid-tree.json').read_text())
for row in tree['req'] + tree['res']:
    raw = subprocess.run(
        ['git', '-C', str(repo), 'cat-file', 'blob', row['sha']],
        check=True, stdout=subprocess.PIPE,
    ).stdout
    (blobs / (row['sha'] + '.json')).write_bytes(raw)
validator = subprocess.run(
    ['git', '-C', str(repo), 'show', tree['sha'] + ':tools/hybrid_loop_bridge.py'],
    check=True, stdout=subprocess.PIPE,
).stdout
(scratch / 'pinned-validator.py').write_bytes(validator)
PY
python mission/continuations/audit_hybrid_reconciliation.py \
  --tree mission/continuations/2026-10-08-hybrid-tree.json \
  --blobs "$ICARUS_AUDIT_SCRATCH/blobs" \
  --validator "$ICARUS_AUDIT_SCRATCH/pinned-validator.py" \
  --validator-blob-sha f4ecdfdd0c8448245b8b7dadb43a1ccec7b5462f \
  --output "$ICARUS_AUDIT_SCRATCH/reproduced-report.json"
```

The audit timestamp will differ. The recorded validator input came through a text transport with one extra EOF newline; that byte was excluded only after matching the original Git blob SHA. An exact `git show` input has no transport adjustment. Compare counts, identities, ordering, issues and source hashes rather than those two transport/time fields.

This auditor is a bounded reconciliation of the recorded schema and pinned source. Its syntactic validity does not prove prior worker cognition, source correctness, historical readback, licensed scope or consumer integration. Five BLOCKED results and the legacy schema-invalid Alpha NO_MATERIAL_DELTA file remain historical evidence; they are not upgraded or rewritten by this audit.
