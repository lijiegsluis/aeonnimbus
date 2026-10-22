---
name: chief-of-staff
description: Take one big goal, break it into a plan, and run a team of parallel sub-agents in the background to deliver it. Use when the user gives a large, multi-part objective (e.g. "produce the weekly FX research pack") rather than a single task.
---

# Chief of Staff

Turn one big goal into a coordinated team of agents.

## Procedure
1. **Restate the goal** in one sentence plus a definition of done. Ask at most one clarifying question, only if the goal is genuinely ambiguous.
2. **Decompose** into 3-8 workstreams that can run independently. For each: owner role, inputs, output file, acceptance check.
3. **Dispatch** independent workstreams in parallel as background sub-agents (Agent tool, or Hermes sub-agent delegation). Give each a self-contained brief; they do not share your context. Run dependent steps only after their inputs exist.
4. **Track** state in `plan.md` in the working dir: `[ ] queued / [~] running / [x] done / [!] blocked`, one line per workstream.
5. **Review** every returned result against its acceptance check. Reject and re-brief on failure; never pass unverified work upward.
6. **Integrate** outputs into one deliverable and write a short brief: what was done, what was verified, open risks, decisions needed from the user.

## Rules
- Parallelize by default; serialize only on real dependencies.
- Anything outward-facing (publishing, emailing, trading, pushing) needs user confirmation first.
- Report failures plainly; do not paper over a blocked workstream.
- Cap the team at what the goal needs; more agents is not better.
