# TrueBench Agentic Bench Intelligence Network

**Track 2 (Vibing + Grounding) submission — Agentic AI Hackathon: Build with Neuro® AI Multi-Agent Accelerator (neuro-san), Cognizant AI Lab, Sept 2026.**

A multi-agent bench, redeployment, and talent-visibility system built entirely on the **Neuro SAN** framework: one front-man orchestrator, six domain-specialist agents, a dedicated governance/evaluation-loop agent, and a shared communications agent — all declared in a single HOCON agent network, backed by Python coded tools.

This is a from-scratch reimplementation of the TrueBench concept **as a real Neuro SAN agent network**, not a UI mockup: every fact an agent states is grounded in a coded-tool call over an in-memory synthetic dataset, never invented by the LLM.

---

## 1. Why this problem

Bench/redeployment management is a real, recurring, high-cost coordination problem (see `docs/PROJECT_SUMMARY.md` for the full case): stale self-reported skill profiles hide qualified people from open roles, "shadow bench" associates read as 100% allocated while doing a fraction of expected work, and RMG coordinators do most of the matching, tracking, and outreach by hand. TrueBench automates the reasoning; a human still approves every action.

## 2. Agent network architecture

```
                         ┌───────────────────────┐
              user  ───▶ │ truebench_orchestrator│  (front-man)
                         └───────────┬───────────┘
           ┌───────────┬─────────────┼─────────────┬───────────┬─────────────┐
           ▼           ▼             ▼              ▼           ▼             ▼
  skill_verification talent_matching shadow_bench  allocation  retention   savings_ledger
     _agent            _agent         _agent      _planning     _risk        _agent
        │                │  \           │  \        _agent      _agent         │
        ▼                ▼   \          ▼   \          │           ▼            ▼
 SkillExtractorTool MatchScoreTool \ShadowUtilTool\   ┌─┴─┐   FlightRiskTool SavingsLedgerTool
                              \      \              ▼   ▼
                               \      \      AllocationPlannerTool  plan_validator_agent
                                \      \                                │  (evaluation loop)
                                 \      \                                ▼
                                  ▼      ▼                        ComplianceCheckTool
                              communication_agent  (shared downstream agent)
```

- **Multi-agent orchestration**: the front-man routes free-text questions to 1+ of six specialists based on intent, then synthesizes their answers — a real AAOSA-style delegation network, not a single prompt.
- **Tool-using agents**: every specialist's factual claims are grounded by a Python `CodedTool` call (skill diffing, fit scoring, utilization math, allocation planning, flight-risk scoring, savings computation) rather than left to LLM recall.
- **Reasoning / evaluation loop**: `allocation_planning_agent` cannot present a plan to the user without first routing it through `plan_validator_agent`, a dedicated governance checkpoint that runs a deterministic `ComplianceCheckTool` (human-in-the-loop framing, bias-safe evidence, explainability, capacity-not-blame language) and can fail the plan back for revision.
- **DAG, not just a tree**: `communication_agent` is a shared downstream agent called by both `talent_matching_agent` and `shadow_bench_agent`, demonstrating agent reuse across the network as covered in the Neuro SAN tutorial.

| File | Role |
|---|---|
| `registries/truebench/truebench_agent_network.hocon` | The full agent network: LLM config, AAOSA instructions, all 9 agents + their tool wiring |
| `registries/manifest.hocon` | Registers the network with the neuro-san server |
| `coded_tools/truebench_agent_network/data.py` | Shared, fully synthetic in-memory dataset (people, requisitions, evidence) |
| `coded_tools/truebench_agent_network/*.py` | One `CodedTool` per specialist's grounding logic |

## 3. Technology requirements compliance

- **Core framework**: Neuro SAN / Neuro SAN Studio, as required for Track 2.
- **Data**: 100% synthetic, invented for this demo — no PII, no real employees, no confidential data (per hackathon Data Usage Rules).
- **Open-source only**: no proprietary components; LLM provider is swappable (OpenAI/Anthropic/Gemini) via `llm_config.model_name`, matching the framework's LLM-agnostic design.

## 4. Setup & running it

```bash
# 1. Clone the Neuro SAN Studio runner alongside this repo's registries/coded_tools
git clone https://github.com/cognizant-ai-lab/neuro-san-studio
cd neuro-san-studio
python -m venv venv && source venv/bin/activate    # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# 2. Copy this repo's registries/ and coded_tools/ folders into your neuro-san-studio
#    checkout (or point the env vars below at this repo's copies directly).
cp -r /path/to/truebench-agentic/registries/truebench   ./registries/
cp -r /path/to/truebench-agentic/registries/manifest.hocon ./registries/manifest.hocon
cp -r /path/to/truebench-agentic/coded_tools/truebench_agent_network ./coded_tools/

# 3. Set your LLM provider key (see .env.example) — default config expects OPENAI_API_KEY.
export OPENAI_API_KEY="<your-key>"
# Free-tier options: https://github.com/cheahjs/free-llm-api-resources

# 4. Point the server at this agent network and run it
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
export AGENT_TOOL_PATH="./coded_tools"
python -m neuro_san_studio run
```

Then select **`truebench/truebench_agent_network`** in the web client (nsflow or MAUI) and try the sample queries in `docs/demo_script.md`.

To switch LLM providers, change `model_name` in the top of `truebench_agent_network.hocon` (e.g. `claude-sonnet-4-5`, `gemini-2.5-flash`) and set the matching API key — no other change needed, per the framework's LLM-agnostic design.

## 5. How this maps to the judging criteria

| Criteria | Where to look |
|---|---|
| **Problem Relevance** | `docs/PROJECT_SUMMARY.md` §1 — real, recurring bench/redeployment coordination cost |
| **Innovation** | Ground-truth skill verification vs. stale profiles; computed (not asserted) shadow-bench detection; a dedicated evaluation-loop agent gating every allocation plan |
| **Effective Use of Neuro SAN** | 9-agent HOCON network with AAOSA delegation, a shared downstream agent (DAG), and 7 coded tools — see §2 above and the `.hocon` file itself |
| **Technical Implementation** | Working, importable `CodedTool` classes with clear separation of data / logic / agent instructions; see `coded_tools/truebench_agent_network/` |
| **Impact Potential** | `docs/PROJECT_SUMMARY.md` §3 — scales to any org's real bench data by swapping `data.py` for a live HRIS/PSA feed |
| **Presentation** | `docs/PROJECT_SUMMARY.md` (1–2 page summary) + `docs/demo_script.md` (ready-to-run demo queries for the live demo / recording) |

## 6. Submission checklist (per hackathon rules §6)

- [x] Working prototype — this agent network, runnable against neuro-san-studio
- [x] Source code repository — this zip, ready to push to GitHub
- [x] Architecture description — `docs/ARCHITECTURE.md`
- [ ] Short demo video or live demonstration — record using the walkthrough in `docs/demo_script.md`
- [x] Project summary (1–2 pages) — `docs/PROJECT_SUMMARY.md`

## 7. Data & IP notes

All data in `data.py` is synthetic and invented for this hackathon; no PII, financial, medical, or confidential organizational data is used, per the hackathon's Data Usage Rules. This repo is released under Apache-2.0 in keeping with Neuro SAN's own license; per the hackathon's IP terms, any components derived directly from the Neuro SAN platform remain the property of Cognizant AI Lab, while the original agent designs, tool logic, and instructions here are retained by the author.
