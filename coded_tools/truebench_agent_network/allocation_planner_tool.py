"""
allocation_planner_tool.py — backs the `allocation_planning_agent`.

Produces a greedy, best-fit weekly allocation plan across every open requisition,
drawing from bench associates, eligible new joiners, and reclaimable shadow-bench
associates, flagging any requisition with no qualifying internal candidate as a
genuine external-hire recommendation. This is TrueBench's "AI plan that commits."

The `allocation_planning_agent` is expected to hand this plan to the
`plan_validator_agent` (a governance/evaluation-loop sub-agent) before presenting it
to a human for approval — see `compliance_check_tool.py`.
"""

from typing import Any, Dict, List, Set

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.truebench_agent_network.data import (
    BENCH_PEOPLE,
    NEW_JOINERS,
    REQUISITIONS,
    SHADOW_BENCH,
)


def _coverage(skills: List[str], req_skills: List[str]) -> float:
    if not req_skills:
        return 0.0
    return len([s for s in req_skills if s in skills]) / len(req_skills)


class AllocationPlannerTool(CodedTool):
    """Greedy best-fit allocation across all open requisitions."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        candidate_pool = [
            {**p, "source": "bench"} for p in BENCH_PEOPLE
        ] + [
            {**p, "source": "new_joiner"} for p in NEW_JOINERS
        ] + [
            {**p, "source": "shadow_bench"} for p in SHADOW_BENCH
        ]

        taken: Set[str] = set()
        plan: List[Dict[str, Any]] = []
        cleared_critical = 0
        reclaimed_fte = 0.0

        # Requisitions ordered so the hardest-to-fill / most senior roles get first pick.
        for req in sorted(REQUISITIONS, key=lambda r: -r["level"]):
            best = None
            best_cov = 0.0
            for cand in candidate_pool:
                if cand["id"] in taken:
                    continue
                if cand["source"] == "new_joiner" and not req["fresher_ok"]:
                    continue
                cov = _coverage(cand.get("verified_skills", []), req["skills"])
                if cov >= 0.55 and cov > best_cov:
                    best, best_cov = cand, cov

            if best:
                taken.add(best["id"])
                if best["source"] == "bench" and best.get("bench_days", 0) >= 45:
                    cleared_critical += 1
                if best["source"] == "shadow_bench":
                    reclaimed_fte += round((1 - best["logged_hrs"] / best["expected_hrs"]) * 100) / 100
                plan.append({
                    "requisition": req["role"], "client": req["client"], "req_id": req["id"],
                    "assigned_to": best["name"], "source": best["source"],
                    "fit_pct": round(best_cov * 100),
                    "missing_skills": [s for s in req["skills"] if s not in best.get("verified_skills", [])],
                })
            else:
                plan.append({
                    "requisition": req["role"], "client": req["client"], "req_id": req["id"],
                    "assigned_to": None, "source": None,
                    "recommendation": "external hire — no qualifying internal candidate",
                })

        internal_fill = sum(1 for row in plan if row.get("assigned_to"))
        return {
            "plan": plan,
            "requisitions_total": len(REQUISITIONS),
            "internal_fill_count": internal_fill,
            "external_hire_count": len(REQUISITIONS) - internal_fill,
            "critical_bench_cleared": cleared_critical,
            "shadow_fte_reclaimed": round(reclaimed_fte, 2),
            "status": "DRAFT — must pass governance/compliance review before human approval.",
        }

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(args, sly_data)
