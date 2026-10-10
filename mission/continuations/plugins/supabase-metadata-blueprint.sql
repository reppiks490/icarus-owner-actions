-- UNAPPLIED; UNVALIDATED ON POSTGRESQL; DESIGN EXAMPLE ONLY.
-- Not a migration. No connected database was queried or changed.
-- GitHub reppiks490/icarus-owner-actions, branch main, file mission/register.json, alone owns mission status.
-- Requires review of actual role ownership, inheritance, and exposed schemas.
-- This schema MUST remain excluded from Data API exposed schemas.
-- Running this example ends in ROLLBACK and grants no runtime access.

begin;

create schema icarus_support_private;
revoke all on schema icarus_support_private
  from public, anon, authenticated, service_role;

-- Applies to objects subsequently created by the role executing this statement.
alter default privileges in schema icarus_support_private
  revoke all on tables from public, anon, authenticated, service_role;
alter default privileges in schema icarus_support_private
  revoke all on sequences from public, anon, authenticated, service_role;
alter default privileges in schema icarus_support_private
  revoke execute on functions from public, anon, authenticated, service_role;

create table icarus_support_private.evidence_metadata (
  local_evidence_id uuid primary key,
  canonical_repository text not null
    check (canonical_repository = 'reppiks490/icarus-owner-actions'),
  canonical_branch text not null check (canonical_branch = 'main'),
  canonical_commit_sha text not null check (canonical_commit_sha ~ '^[0-9a-f]{40}$'),
  evidence_kind text not null
    check (evidence_kind in ('documentation', 'local_validation', 'review_note')),
  sanitized_artifact_sha256 text not null
    check (sanitized_artifact_sha256 ~ '^[0-9a-f]{64}$'),
  observed_at timestamptz not null
);

revoke all on table icarus_support_private.evidence_metadata
  from public, anon, authenticated, service_role;
alter table icarus_support_private.evidence_metadata enable row level security;
alter table icarus_support_private.evidence_metadata force row level security;

-- Deliberately no policies or worker grants: deny by default.
-- No mission-status column, free-form payload, provider identifier, or URL.
-- FORCE RLS does not constrain superusers or BYPASSRLS roles.
rollback;
