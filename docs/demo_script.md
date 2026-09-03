# Demo Script — TrueBench Agentic Bench Intelligence Network

Use these queries against `truebench_orchestrator` (via nsflow or MAUI) to demonstrate every
agent and both coded-tool grounding and the evaluation loop. Recommended order for a
live demo or recording, with what each query proves:

## 1. Ground-truth skill verification
> **"What does the evidence say about Wei L.'s real skills, and what does his official profile say?"**

Proves: `skill_verification_agent` → `SkillExtractorTool`. Expect the answer to name the stale
profile ("Python" only) vs. verified skills (Python, Data Eng, Snowflake, AWS) and list which
open role(s) that unlocks.

## 2. Talent matching (person → roles)
> **"What roles is Priya N. a strong match for?"**

Proves: `talent_matching_agent` → `MatchScoreTool`. Expect a ranked list with fit % and any
missing skills, topped by the Senior React Engineer role.

## 3. Talent matching (role → candidates) + combined reasoning
> **"Who should I interview first for the DevOps / Kubernetes role, and is anyone's profile hiding a better fit than it looks?"**

Proves: the orchestrator calling **two** specialists (`talent_matching_agent` +
`skill_verification_agent`) and synthesizing both into one answer — the clearest single query
to show multi-agent orchestration + reasoning in one shot.

## 4. Shadow-bench / hidden capacity
> **"Who on the shadow bench has idle capacity we could reclaim, and who's due for a 12-month review?"**

Proves: `shadow_bench_agent` → `ShadowUtilizationTool`. Expect computed real-utilization %
per person and an explicit call-out of anyone past the 365-day review threshold (Hana S. and
Carlos D. should both be flagged).

## 5. Allocation planning + the evaluation loop (the key demo moment)
> **"Give me this week's full allocation plan across all open roles."**

Proves the whole chain: `allocation_planning_agent` → `AllocationPlannerTool` (draft plan) →
**mandatory** call to `plan_validator_agent` → `ComplianceCheckTool` (governance verdict) →
final answer. Call this out explicitly in the recording: *"the agent cannot show me this plan
without it passing governance validation first — that's the evaluation loop."*

## 6. Retention risk
> **"Who's most likely to resign from the bench right now, and what should I do about it?"**

Proves: `retention_risk_agent` → `FlightRiskTool`. Expect Wei L. (64 days, highly marketable
skills) at or near the top, with one concrete action recommended.

## 7. Savings ledger
> **"How much time and money has TrueBench saved this week?"**

Proves: `savings_ledger_agent` → `SavingsLedgerTool`. Expect an hours/₹ figure with the
blended hourly rate assumption stated explicitly (auditability, not a bare marketing number).

## 8. Shared downstream agent (communication)
> **"Draft an interview invite for Priya N. for the Senior React Engineer role."**

Proves: `talent_matching_agent` delegating to the shared `communication_agent`, showing agent
reuse (the same agent is also reachable from `shadow_bench_agent` for utilization-review
emails) — i.e. a DAG-shaped network, not a strict tree.

---

### Recording tips
- Show the HOCON file briefly (§ agent list) before the first query, so viewers see this is a
  declarative multi-agent network, not a single prompt.
- For query 5, pause on the validator's verdict object specifically — it's the single strongest
  piece of evidence for "evaluation loops" and "governance."
- If using nsflow's Agent Network Diagram tab, keep it open throughout so viewers see which
  agents actually light up per query.
