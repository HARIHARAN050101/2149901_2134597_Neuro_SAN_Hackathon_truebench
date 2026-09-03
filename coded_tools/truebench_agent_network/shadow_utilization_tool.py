"""
shadow_utilization_tool.py — backs the `shadow_bench_agent`.

Computes *real* utilization (logged ÷ expected hours) for associates who show up as
"100% allocated" in every dashboard, surfacing reclaimable FTE, and flags anyone who
has crossed the 12-month annual-utilization-review threshold — TrueBench's "hidden
capacity" detection, computed rather than asserted.
"""

from typing import Any, Dict, List

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.truebench_agent_network.data import SHADOW_BENCH, find_manager

REVIEW_THRESHOLD_DAYS = 365


class ShadowUtilizationTool(CodedTool):
    """Computes reclaimable FTE and 12-month review status for the shadow bench."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        person_ref = args.get("person", "")

        pool = SHADOW_BENCH
        if person_ref:
            pool = [p for p in SHADOW_BENCH if person_ref.lower() in p["name"].lower()]
            if not pool:
                return {"error": f"No shadow-bench associate found matching '{person_ref}'."}

        rows: List[Dict[str, Any]] = []
        total_reclaim = 0.0
        for p in pool:
            real_util = round((p["logged_hrs"] / p["expected_hrs"]) * 100)
            reclaim_fte = round((1 - p["logged_hrs"] / p["expected_hrs"]) * 100) / 100
            total_reclaim += reclaim_fte
            mgr = find_manager(p["mgr_eid"])
            months = round(p["shadow_days"] / 30, 1)
            rows.append({
                "name": p["name"], "level": p["level"], "project": p["project"],
                "phase": p["phase"], "logged_hrs": p["logged_hrs"], "expected_hrs": p["expected_hrs"],
                "real_utilization_pct": real_util, "reclaimable_fte": reclaim_fte,
                "months_on_project": months, "manager": mgr["name"] if mgr else p["mgr_eid"],
                "review_due": p["shadow_days"] >= REVIEW_THRESHOLD_DAYS,
            })

        return {
            "shadow_bench_rows": rows,
            "total_reclaimable_fte": round(total_reclaim, 2),
            "review_threshold_days": REVIEW_THRESHOLD_DAYS,
            "note": (
                "Utilization is computed live from logged-vs-expected hours, never a "
                "pre-set status. This is capacity insight for redeployment, not "
                "individual performance judgment."
            ),
        }

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(args, sly_data)
