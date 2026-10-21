"""One finite Icarus 2 metadata cycle; no autonomous trading or publication."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat

MAX_INPUT_BYTES = 64 * 1024 * 1024


def _read_snapshot(path: Path):
    if os.name != 'posix' or not hasattr(os, 'O_NOFOLLOW'):
        raise ValueError('secure snapshot file access unavailable')
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as handle:
        info = os.fstat(handle.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_INPUT_BYTES:
            raise ValueError('invalid snapshot input')
        raw = handle.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError('snapshot input bound')
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError('duplicate snapshot key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite snapshot number')))


def _write_exclusive(path: Path, document):
    raw = (json.dumps(document, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(descriptor, 'wb') as handle:
        handle.write(raw)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sources = parser.add_mutually_exclusive_group(required=True)
    sources.add_argument('--snapshot', type=Path, help='Validate an already captured metadata snapshot')
    sources.add_argument('--collect', action='store_true', help='Read current canonical GitHub metadata once')
    parser.add_argument('--cycle-id', help='Explicit identity for a new collection cycle')
    parser.add_argument('--output-dir', type=Path, required=True, help='New directory for immutable local evidence')
    parser.add_argument('--require-validated', action='store_true', help='Return failure for incomplete or drifting snapshots')
    args = parser.parse_args(argv)
    try:
        if args.output_dir.exists() or args.output_dir.is_symlink():
            raise ValueError('immutable output already exists')
        if args.collect:
            from .transport import collect_snapshot
            snapshot = collect_snapshot(cycle_id=args.cycle_id)
        else:
            snapshot = _read_snapshot(args.snapshot)
        from .core import build_cycle
        cycle = build_cycle(snapshot)
        args.output_dir.mkdir(mode=0o700, parents=False, exist_ok=False)
        _write_exclusive(args.output_dir/'snapshot.json', snapshot)
        _write_exclusive(args.output_dir/'cycle.json', cycle)
        print(json.dumps({'cycle_id': cycle['cycle_id'], 'status': cycle['status'],
            'metadata_only': True, 'execution_authorized': False, 'published_to_github': False}))
        return 2 if args.require_validated and cycle['status'] != 'SNAPSHOT_VALIDATED' else 0
    except (OSError, ValueError, TypeError, KeyError, RecursionError, OverflowError):
        print(json.dumps({'status':'CYCLE_CAPTURE_FAILED','execution_authorized':False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
