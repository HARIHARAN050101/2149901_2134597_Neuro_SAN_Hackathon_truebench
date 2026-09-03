# Architecture Description — TrueBench Agentic Bench Intelligence Network

## 1. Overview

TrueBench is implemented as a single Neuro SAN **agent network** (one HOCON file), composed of:

- **1 front-man agent** (`truebench_orchestrator`) — the only agent the user talks to directly.
- **6 top-level specialist agents**, each owning one domain of the bench-management problem.
- **1 evaluation-loop / governance agent** (`plan_validator_agent`), reachable only from the allocation planner.
- **1 shared downstream agent** (`communication_agent`), reachable from two different specialists.
- **7 Python `CodedTool` classes**, each grounding exactly one specialist's factual claims in a shared in-memory dataset.

This is a **DAG-shaped**, not tree-shaped, network: `communication_agent` has two parents, and `plan_validator_agent` sits strictly between a tool call and the human, rather than being just another peer specialist.

## 2. Agent-by-agent responsibilities

| Agent | Type | Delegates to | Responsibility |
|---|---|---|---|
| `truebench_orchestrator` | Front-man (LLM) | all 6 specialists | Intent routing + synthesis of one or more specialist answers into a single response |
| `skill_verification_agent` | Specialist (LLM) | `SkillExtractorTool` | Diff a person's stale, self-reported skills against their verified skills inferred from real project/ticket evidence |
| `talent_matching_agent` | Specialist (LLM) | `MatchScoreTool`, `communication_agent` | Rank roles for a person, or candidates for a role, by verified-skill fit; optionally draft outreach |
| `shadow_bench_agent` | Specialist (LLM) | `ShadowUtilizationTool`, `communication_agent` | Detect idle capacity inside "fully allocated" project teams; flag 12-month utilization reviews; optionally draft the review email |
| `allocation_planning_agent` | Specialist (LLM) | `AllocationPlannerTool`, `plan_validator_agent` | Produce a whole-board weekly allocation plan, then **must** pass it through governance validation before it can be shown to the user |
| `retention_risk_agent` | Specialist (LLM) | `FlightRiskTool` | Score bench associates by flight risk; prescribe retention actions for the top cases |
| `savings_ledger_agent` | Specialist (LLM) | `SavingsLedgerTool` | Compute automation time/cost savings and the manual-vs-tool efficiency baseline |
| `plan_validator_agent` | Evaluation loop (LLM) | `ComplianceCheckTool` | Deterministically checks a draft plan against governance rules; returns pass/fail + violations, unfiltered, back up-chain |
| `communication_agent` | Shared leaf (LLM) | — | Drafts short, fact-grounded outreach/review messages for whichever specialist calls it |

Each `*Tool` entry in the table above is a Python `CodedTool` (see §4); everything else is a pure LLM-based agent defined declaratively in the HOCON file.

## 3. Why an explicit evaluation loop

`allocation_planning_agent`'s instructions make the `plan_validator_agent` call **mandatory**, not optional: step 1 produces a draft plan, step 2 requires validation, step 3 requires the agent to surface — never suppress — any reported violation. `plan_validator_agent` in turn calls a deterministic, rule-based `ComplianceCheckTool` rather than another LLM judgment call, so the checkpoint cannot be talked out of catching a violation the way a second LLM opinion sometimes can be. This is the network's concrete answer to the hackathon's "evaluation loops" requirement: a plan is not presentable to a human approver until it has passed a checkpoint that is structurally separate from the agent that produced it.

## 4. Coded tools — data flow

```
data.py  (synthetic dataset: BENCH_PEOPLE, NEW_JOINERS, SHADOW_BENCH, REQUISITIONS,
          MANAGERS, EVIDENCE, BLENDED_RATE_PER_HOUR + lookup helpers)
   │
   ├── skill_extractor_tool.py      → diff stale vs. verified skills, list newly-unlocked roles
   ├── match_score_tool.py          → verified-skill fit % between people ⇄ requisitions
   ├── shadow_utilization_tool.py   → logged/expected hours → reclaimable FTE, 12-mo review flag
   ├── allocation_planner_tool.py   → greedy best-fit whole-board plan (bench + new joiners + shadow)
   ├── compliance_check_tool.py     → rule-based pass/fail over a draft plan's rows
   ├── flight_risk_tool.py          → bench-days × skill-marketability risk score
   └── savings_ledger_tool.py       → hours/₹ saved + manual-vs-tool efficiency %
```

Every tool imports its inputs from the single `data.py` module, so every agent in the network reasons over one consistent, live "company" state during a session — there is no risk of one agent's answer disagreeing with another's about the same underlying facts.

## 5. Request lifecycle (example)

**User → `truebench_orchestrator`**: *"Who should I interview first for the DevOps role, and is anyone's profile hiding a better fit?"*

1. Orchestrator recognizes two intents: matching + skill verification.
2. Calls `talent_matching_agent` → `MatchScoreTool(requisition="DevOps / Kubernetes Eng.")` → ranked candidate list with fit %.
3. Calls `skill_verification_agent` → `SkillExtractorTool(person=<top candidates>)` → confirms whether any candidate's official profile understates them.
4. Orchestrator synthesizes both results into one answer, naming real candidates, their fit %, and any profile-vs-evidence gap.

**User → `truebench_orchestrator`**: *"Give me this week's allocation plan."*

1. Orchestrator → `allocation_planning_agent`.
2. `allocation_planning_agent` → `AllocationPlannerTool` → draft plan (10 rows, some external-hire flags).
3. `allocation_planning_agent` → `plan_validator_agent` → `ComplianceCheckTool(plan=...)` → verdict.
4. If `passed: true`, the plan is returned as ready for human approval; if `false`, the flagged rows are called out explicitly as needing revision before approval.

## 6. Extensibility

- Swapping `data.py` for a live HRIS/PSA/ATS data source (via a REST-calling `CodedTool`) requires no change to any agent's HOCON instructions — the agents reason over whatever the tool returns.
- Adding a new specialist (e.g. a "Client Sentiment Agent") is a matter of adding one more agent block to `tools` on `truebench_orchestrator` plus its own coded tool — the rest of the network is unaffected.
- The `plan_validator_agent` pattern (LLM agent → deterministic rule-based tool → unfiltered verdict passed up-chain) can be reused as a governance checkpoint in front of any other agent's output, not just the allocation planner.
