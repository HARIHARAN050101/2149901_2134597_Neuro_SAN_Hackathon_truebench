"""
flight_risk_tool.py — backs the `retention_risk_agent`.

Computes a flight-risk score per bench associate from days-on-bench × how easily their
verified skills could be poached elsewhere (skill marketability) — TrueBench's
"Retention radar." The score is computed, not asserted, and drops the moment an
associate gets scheduling/allocation activity, which the calling agent can pass in via
`has_recent_activity`.
"""

from typing import Any, Dict, List

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.truebench_agent_network.data import BENCH_PEOPLE

# Simple, transparent marketability weights per skill (higher = more in-demand externally).
MARKETABILITY = {
    "React": 0.85, "AWS": 0.9, "Node.js": 0.8, "Java": 0.75, "Spring Boot": 0.75,
    "Kubernetes": 0.95, "Python": 0.85, "Data Eng": 0.85, "Snowflake": 0.85,
    ".NET": 0.6, "Azure": 0.75, "SQL": 0.5, "Salesforce": 0.7, "Terraform": 0.9,
}


def _marketability(skills: List[str]) -> float:
    if not skills:
        return 0.3
    return sum(MARKETABILITY.get(s, 0.5) for s in skills) / len(skills)


class FlightRiskTool(CodedTool):
    """Computes flight-risk scores for bench associates."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        active_ids = set(args.get("active_person_ids", []))  # ids with recent interview/allocation

        rows = []
        for p in BENCH_PEOPLE:
            market = _marketability(p.get("verified_skills", []))
            raw_score = min(100, round((p["bench_days"] / 65) * 60 + market * 40))
            is_active = p["id"] in active_ids
            score = max(5, raw_score - 35) if is_active else raw_score
            level = "high" if score >= 65 else "medium" if score >= 40 else "low"
            rows.append({
                "name": p["name"], "bench_days": p["bench_days"],
                "skill_marketability": round(market, 2), "flight_risk_score": score,
                "risk_level": level, "stabilising_activity": is_active,
                "driver": f"{p['bench_days']}d on bench × marketable skills "
                          f"({', '.join(p['verified_skills'])})",
            })

        rows.sort(key=lambda r: -r["flight_risk_score"])
        return {
            "rows": rows,
            "at_risk_now": [r["name"] for r in rows if r["risk_level"] == "high" and not r["stabilising_activity"]],
            "note": "Score = days on bench × skill marketability; scheduling or allocating "
                    "someone drops it live — pass their id in active_person_ids to reflect that.",
        }

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(args, sly_data)
