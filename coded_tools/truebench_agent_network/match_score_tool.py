"""
match_score_tool.py — backs the `talent_matching_agent`.

Computes verified-skill-fit percentages between a person (bench associate or new
joiner) and every open requisition, or between a specific requisition and every
eligible candidate — the core matching computation that TrueBench's front-man agent
relies on before it reasons about who to interview or deploy.
"""

from typing import Any, Dict, List

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.truebench_agent_network.data import (
    BENCH_PEOPLE,
    NEW_JOINERS,
    REQUISITIONS,
    find_person,
    find_requisition,
)


def _fit(skills: List[str], req_skills: List[str]) -> Dict[str, Any]:
    matched = [s for s in req_skills if s in skills]
    missing = [s for s in req_skills if s not in skills]
    coverage = len(matched) / len(req_skills) if req_skills else 0.0
    return {"fit_pct": round(coverage * 100), "matched": matched, "missing": missing}


class MatchScoreTool(CodedTool):
    """Ranks a person against roles, or ranks candidates against a role."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        person_ref = args.get("person", "")
        req_ref = args.get("requisition", "")

        if person_ref:
            person = find_person(person_ref)
            if person is None:
                return {"error": f"No person found matching '{person_ref}'."}
            skills = person.get("verified_skills", [])
            is_new_joiner = person in NEW_JOINERS
            ranked = []
            for r in REQUISITIONS:
                if is_new_joiner and not r["fresher_ok"]:
                    continue
                m = _fit(skills, r["skills"])
                if m["fit_pct"] > 0:
                    ranked.append({"requisition": r["role"], "client": r["client"],
                                    "req_id": r["id"], **m})
            ranked.sort(key=lambda x: -x["fit_pct"])
            return {
                "person": person["name"],
                "verified_skills": skills,
                "ranked_roles": ranked[:10],
                "best_fit": ranked[0] if ranked else None,
            }

        if req_ref:
            req = find_requisition(req_ref)
            if req is None:
                return {"error": f"No requisition found matching '{req_ref}'."}
            candidates = BENCH_PEOPLE + (NEW_JOINERS if req["fresher_ok"] else [])
            ranked = []
            for p in candidates:
                m = _fit(p.get("verified_skills", []), req["skills"])
                if m["fit_pct"] > 0:
                    ranked.append({"candidate": p["name"], "level": p["level"],
                                    "loc": p["loc"], **m})
            ranked.sort(key=lambda x: -x["fit_pct"])
            return {
                "requisition": req["role"],
                "client": req["client"],
                "required_skills": req["skills"],
                "ranked_candidates": ranked[:10],
            }

        return {"error": "Provide either 'person' or 'requisition' to match against."}

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(args, sly_data)
