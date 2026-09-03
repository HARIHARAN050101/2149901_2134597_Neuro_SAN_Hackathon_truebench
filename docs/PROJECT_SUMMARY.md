# Project Summary — TrueBench Agentic Bench Intelligence Network

**Agentic AI Hackathon: Build with Neuro® AI Multi-Agent Accelerator (neuro-san) — Track 2**
**Cognizant AI Lab, Sept 2026**

## 1. Problem relevance

Every delivery organization with a bench faces the same coordination failure, regardless of size:

- **Stale profiles hide real skills.** Skill profiles are typically written once, at onboarding, and never updated. An associate whose last two projects made them a strong AWS/React engineer may still be listed under the two-year-old skills from their original role, so matching systems and managers never see them for roles they'd win.
- **"Shadow bench" hides idle capacity.** Associates who are 100% allocated on paper can be logging a fraction of expected hours on a project in maintenance, ramp-down, or post-go-live phase — capacity that never gets reclaimed because no dashboard distinguishes "allocated" from "actually working."
- **New joiners are invisible to normal matching**, because they have academy training and a capstone project but no "project history" for a resume-keyword matcher to key off of.
- **RMG/Talent teams absorb all of this manually** — screening, ranking, scheduling, tracking, and reporting — with no automation and no single source of truth.

This is not a hypothetical: it is the day-to-day workload of every delivery-manager and RMG-coordinator role in a large services organization, and it directly affects bench cost, time-to-deploy, and attrition of benched talent.

## 2. What we built

A **Neuro SAN agent network** — not a chatbot wrapper, and not a UI mockup — with nine agents:

- A **front-man orchestrator** that routes free-text questions to the right specialist(s).
- Six **domain specialists**: skill verification (ground-truth vs. stale profile), talent matching (verified-skill fit), shadow-bench detection (computed real utilization), allocation planning (whole-board weekly plan), retention risk (flight-risk scoring), and a savings ledger (automation ROI, computed transparently).
- A dedicated **evaluation-loop / governance agent** (`plan_validator_agent`) that every allocation plan must pass through — deterministically checking human-in-the-loop framing, bias-safe evidence, explainability, and non-punitive language — before a plan can be shown to a human approver.
- A **shared communications agent**, reused by two different specialists to draft outreach and utilization-review messages strictly from the facts it's given.

Every specialist is backed by a Python `CodedTool` that computes its answer from a shared, fully synthetic in-memory dataset (bench associates, new joiners, shadow-bench associates, managers, open requisitions, and project/ticket evidence text) — so every number an agent states (a fit %, an hours-logged figure, a flight-risk score) is computed, not hallucinated.

## 3. Innovation & impact potential

The two ideas we think are genuinely distinctive:

1. **Ground-truth skill verification as a first-class agent**, not a side feature — the network treats "what does the evidence actually say about this person" as its own specialist with its own tool, specifically because stale profiles are the root cause of most missed internal matches.
2. **A structurally separate evaluation loop for AI-generated plans.** Rather than trusting the same agent that drafted an allocation plan to also judge it, the plan is routed through a second agent that calls a deterministic, rule-based validator. This is a general pattern — any agent's output can be gated behind the same kind of checkpoint — and it directly demonstrates the "evaluation loops" capability the hackathon calls for, in a way that is auditable rather than another LLM's opinion.

**Scaling this beyond the demo** requires no change to any agent's instructions: replace `data.py`'s synthetic lists with a `CodedTool` that calls a real HRIS/PSA/ATS API, and every agent in the network reasons over live company data instead. The governance checkpoint pattern is reusable in front of any other agent whose output needs a human-approval gate (e.g. layoff recommendations, compensation changes) — anywhere an organization wants "the AI recommends, a person approves" enforced structurally rather than by policy alone.

## 4. Technical approach

- **Framework**: Neuro SAN, declared entirely in one HOCON file (`registries/truebench/truebench_agent_network.hocon`) using the AAOSA delegation protocol for autonomous routing between agents.
- **Tools**: 7 Python `CodedTool` implementations, each importing from one shared `data.py` module so all agents in a session see a single consistent state.
- **Data**: 100% synthetic — no PII, no real employees, no confidential data, per the hackathon's data-usage rules.
- **LLM-agnostic**: default config uses `gpt-4o`; swapping to Anthropic or Gemini is a one-line change to `model_name`.

## 5. Demonstrated capabilities (per hackathon objective)

| Requirement | Where it shows up |
|---|---|
| Multi-agent orchestration | 9 agents, front-man delegation, one shared downstream agent (DAG) |
| Tool-using agents | 7 coded tools, one per specialist's grounding logic |
| Reasoning workflows | Multi-intent orchestrator synthesis; allocation plan → validation → human-approval chain |
| Real-world problem solving | Bench redeployment, hidden-capacity reclaim, retention risk, automation ROI — all computed |
