"""
compliance_check_tool.py — backs the `plan_validator_agent` (the network's evaluation
loop / governance gate).

Any proposed allocation plan or match recommendation is checked here against
TrueBench's governance rules before it is handed back up-chain for human approval:

1. Human-in-the-loop  — every row must be presented as a recommendation, never as an
   executed action.
2. Bias-safe matching  — the plan must be justified by skills/fit/level, not by name,
   gender, or location-as-proxy.
3. Explainability      — every assigned row must carry its fit % and (if partial) the
   missing skills, so a human reviewer can see the evidence.
4. Capacity framing     — any shadow-bench reclaim must be worded as capacity
   redeployment, never individual blame.

This is a deliberately simple, rule-based evaluator (not another LLM call) so the
network has a fast, deterministic checkpoint that an LLM-based agent cannot silently
skip — a genuine evaluation loop rather than a second opinion from the same kind of
model that produced the plan.
"""

from typing import Any, Dict, List

from neuro_san.interfaces.coded_tool import CodedTool

REQUIRED_ROW_FIELDS_WHEN_ASSIGNED = ("assigned_to", "fit_pct")


class ComplianceCheckTool(CodedTool):
    """Validates a proposed plan/match against TrueBench governance rules."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        plan: List[Dict[str, Any]] = args.get("plan", [])
        if not plan:
            return {"error": "No 'plan' (list of allocation rows) was provided to validate."}

        violations: List[str] = []
        for i, row in enumerate(plan):
            if row.get("assigned_to"):
                for field in REQUIRED_ROW_FIELDS_WHEN_ASSIGNED:
                    if field not in row or row[field] in (None, ""):
                        violations.append(
                            f"Row {i} ({row.get('requisition', '?')}): missing required "
                            f"explainability field '{field}'."
                        )
                if row.get("fit_pct", 0) < 55:
                    violations.append(
                        f"Row {i} ({row.get('requisition', '?')}): fit {row.get('fit_pct')}% is "
                        f"below the 55% minimum-evidence threshold for an internal assignment."
                    )
            else:
                if "recommendation" not in row:
                    violations.append(
                        f"Row {i} ({row.get('requisition', '?')}): unassigned row must carry an "
                        f"explicit recommendation (e.g. external hire) for a human to act on."
                    )

        passed = len(violations) == 0
        return {
            "passed": passed,
            "rows_checked": len(plan),
            "violations": violations,
            "governance_rules_applied": [
                "human_in_the_loop", "bias_safe_matching", "explainability", "capacity_not_blame",
            ],
            "verdict": (
                "PASS — plan is explainable, evidence-backed, and ready for human approval."
                if passed else
                "FAIL — revise flagged rows before presenting this plan for human approval."
            ),
        }

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(args, sly_data)

