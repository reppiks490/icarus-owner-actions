# Owner contact boundary — 2026-10-16

The owner explicitly requests that AI agents do not send progress pings, routine questions, or manual-work requests while authorized ICARUS work remains in progress. This applies across ICARUS repositories and chats.

## Required behavior

- Continue the authorized work independently and keep coordination, status, evidence, and handoffs on the shared coordination bus.
- Do not ask the owner to run commands, inspect files, restart software, provide routine clarification, or repeat an authorization already given.
- When a dependency blocks one task, record the exact evidence, continue useful non-conflicting work, and leave a handoff for another agent. Do not use a blocker as a reason to stop the broader workstream.
- Return to the owner only after the applicable work is complete, unless the owner explicitly sends a new question or instruction that calls for a response.
- Do not represent an external blocker as solved. If complete closure is impossible without an external provider, account, rights, or runtime action, document the blocker and completed work in a durable handoff before reporting it.

This communication preference does not grant authority to expose credentials, purchase provider entitlements, alter data rights, or enable live broker arming. The separate owner constraint keeps live broker arming disabled; broker connection work remains subject to its own scope and authority rules.
