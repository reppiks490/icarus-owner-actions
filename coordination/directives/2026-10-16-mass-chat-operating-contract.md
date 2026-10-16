# ICARUS Mass-Chat Operating Contract — 2026-10-16

Owner directive: ICARUS is scaling from roughly a dozen collaborating agents/chats toward dozens of concurrent ChatGPT chats. There is no fixed worker cap. This contract applies to every chat that is asked to work on ICARUS.

## Start instruction for a newly activated chat

When the owner tells you to begin, first read:

1. `reppiks490/icarus-owner-actions/coordination/README.md`
2. `reppiks490/icarus-owner-actions/coordination/ACTIVE.md`
3. `reppiks490/icarus-owner-actions/coordination/collisions.json`
4. `reppiks490/icarus-owner-actions/coordination/directives/`
5. The target repository's `AGENTS.md` and state/evidence files.

Then create a unique session record and publish a `PLAN` or `CLAIM` note **before** substantial repository mutation.

## No agent-gated tasks

No task is exclusive to Claude, ChatGPT, Codex, Grok, Atlas, or a named model because of identity alone. Old ownership notes are historical collision-prevention evidence, not permanent locks. Work may be divided, reclaimed, reviewed, or cooperatively continued by another chat as long as the new worker publishes what it intends to do and avoids undeclared path collisions.

## Required communication discipline

Follow the owner's no-routine-contact preference in `coordination/directives/2026-10-16-owner-contact-boundary.md`. Keep the coordination bus current for other agents, but do not send the owner progress pings, routine questions, or requests for manual steps while applicable authorized work remains.

Each chat must keep the shared bus current enough that another chat can answer, without guessing:

- What are you doing now?
- Why are you doing it?
- Which repo/branch/PR are you using?
- Which files or directories do you intend to change?
- What is your current phase: research, planning, coding, testing, fixing, reviewing, waiting, blocked, integration, or verification?
- What are you waiting on, if anything?
- Which other sessions or PRs does your work depend on or benefit?
- What evidence proves the latest claim?
- What should another worker do if it can help?

When waiting on a long CI run, explicitly publish a `WAITING` note. Example: `waiting on Windows CI run 12345; Linux passed; continuing non-conflicting source audit`. Do not go silent merely because one dependency is slow.

## Divide and conquer

Chats should actively look for opportunities to split independent work. Before creating a new subtask, inspect `ACTIVE.md` and reservations. If another session's work can benefit yours, link it as a dependency or publish a `HANDOFF`/cooperation note instead of duplicating it. If two workers need the same path, declare mutual cooperation or choose a different integration boundary.

Independent research, test construction, documentation, adapter work, UI work, source qualification, and verification can run in parallel when their paths and interfaces are explicit.

## Continuous-work expectation

A chat should not stop merely because its first narrow task is done if relevant non-conflicting work remains within the owner directive. After each verified checkpoint, inspect the bus, target repo, tests, runtime evidence, and blockers for the next useful piece of work. Do not manufacture busywork; continue only with evidence-backed, relevant work.

## Completion standard

`COMPLETE` means zero known internal errors for that declared scope and fresh evidence for the claim. External provider/account/license/network constraints remain explicit blockers; they are not renamed as fixed. A green wrapper is insufficient if the underlying receipt says blocked or partial.

## Safety / authority boundary

Live broker arming is temporarily out of scope. Do not enable live execution, bypass execution gates, expose secrets, purchase entitlements, or treat a research/paper adapter as live-authorized. The collaboration fabric does not override security, licensing, data-integrity, or execution controls.
