"""
savings_ledger_tool.py — backs the `savings_ledger_agent`.

Computes (rather than asserts) manual-effort-removed and its rupee value, plus a
manual-vs-tool efficiency baseline across the five recurring RMG tasks TrueBench
automates. All figures are transparent, adjustable assumptions — never hard-coded
marketing numbers.
"""

from typing import Any, Dict, List

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.truebench_agent_network.data import BLENDED_RATE_PER_HOUR

# task -> (manual_minutes, tool_minutes) per occurrence
EFFICIENCY_BASELINE: List[Dict[str, Any]] = [
    {"task": "Find & screen candidates per open role", "manual_min": 40, "tool_min": 6},
    {"task": "Prepare a client-ready profile", "manual_min": 35, "tool_min": 6},
    {"task": "Schedule one interview", "manual_min": 30, "tool_min": 4},
    {"task": "Reclaim hidden idle capacity (per case)", "manual_min": 60, "tool_min": 5},
    {"task": "Weekly bench tracking & report", "manual_min": 120, "tool_min": 10},
]

RMG_WEEKLY_EFFORT_SHARE = 0.6  # these five tasks are ~60% of a coordinator's week


class SavingsLedgerTool(CodedTool):
    """Computes weekly hours/₹ saved and the manual-vs-tool efficiency %."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        activity = args.get("activity_counts", {})
        # Expected keys: auto_applications, applicants_ranked, interviews_booked,
        # allocations_committed, ai_analyses_run  (default all to a light demo week if absent)
        defaults = {
            "auto_applications": 9, "applicants_ranked": 14, "interviews_booked": 4,
            "allocations_committed": 3, "ai_analyses_run": 6,
        }
        counts = {**defaults, **activity}
        minutes_per = {
            "auto_applications": 10, "applicants_ranked": 8, "interviews_booked": 25,
            "allocations_committed": 30, "ai_analyses_run": 20,
        }
        total_minutes = sum(counts[k] * minutes_per[k] for k in minutes_per) + 120  # + weekly report
        hours_saved = round(total_minutes / 60, 1)
        money_saved = round(hours_saved * BLENDED_RATE_PER_HOUR)

        per_task = []
        manual_total = tool_total = 0
        for row in EFFICIENCY_BASELINE:
            manual_total += row["manual_min"]
            tool_total += row["tool_min"]
            pct = round((row["manual_min"] - row["tool_min"]) / row["manual_min"] * 100)
            per_task.append({**row, "effort_removed_pct": pct})
        overall_task_pct = round((manual_total - tool_total) / manual_total * 100)
        blended_weekly_pct = round(overall_task_pct * RMG_WEEKLY_EFFORT_SHARE)

        return {
            "hours_saved_this_week": hours_saved,
            "money_saved_this_week_inr": money_saved,
            "blended_rate_assumption_inr_per_hr": BLENDED_RATE_PER_HOUR,
            "per_task_efficiency": per_task,
            "overall_task_effort_removed_pct": overall_task_pct,
            "estimated_weekly_coordination_effort_removed_pct": blended_weekly_pct,
            "note": "Illustrative estimate from a transparent per-task time assumption, "
                    "not an asserted marketing figure. Grows as more activity is logged.",
        }

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(args, sly_data)
