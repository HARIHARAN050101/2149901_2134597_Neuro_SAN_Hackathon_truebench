"""
skill_extractor_tool.py — backs the `skill_verification_agent`.

Given a person (by id/name) or raw free-text evidence, infers the *ground-truth* skill
set and contrasts it against the stale, self-reported profile — the core "Ground-truth
Skill Engine" capability of TrueBench. The LLM-facing agent supplies the reasoning about
what the evidence implies; this tool supplies the deterministic lookup, diffing, and
"how many roles does this unlock" computation so the agent's answer is grounded in real
data rather than invented.
"""

from typing import Any, Dict, List

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.truebench_agent_network.data import (
    BENCH_PEOPLE,
    EVIDENCE,
    REQUISITIONS,
    find_person,
)


class SkillExtractorTool(CodedTool):
    """Looks up a bench associate's stale vs. verified skill profile and evidence."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        person_ref = args.get("person", "")
        evidence_text = args.get("evidence_text", "")

        person = find_person(person_ref) if person_ref else None

        if person is None and not evidence_text:
            names = ", ".join(p["name"] for p in BENCH_PEOPLE)
            return {
                "error": f"No matching person found for '{person_ref}'. "
                         f"Known bench associates: {names}."
            }

        if person is not None:
            verified = person.get("verified_skills", [])
            official = person.get("official_skills", [])
            evidence = EVIDENCE.get(person["id"], "No stored project/ticket evidence on file.")
        else:
            # Freeform evidence with no known person on file.
            verified, official, evidence = [], [], evidence_text

        unlocked = [
            r["role"] for r in REQUISITIONS
            if any(skill in verified for skill in r["skills"])
        ]

        return {
            "person": person["name"] if person else "unlisted / custom evidence",
            "stale_self_reported_skills": official,
            "verified_skills_from_evidence": verified,
            "evidence_used": evidence,
            "newly_visible_for_roles": unlocked,
            "note": (
                "Verified skills come from actual project/ticket history, not the "
                "self-reported profile. Use this diff to explain why a match may have "
                "been missed previously."
            ),
        }

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(args, sly_data)
