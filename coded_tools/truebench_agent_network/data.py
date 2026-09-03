"""
data.py — shared, fully synthetic in-memory dataset for the TrueBench agent network.

No real employees, no PII, no proprietary or confidential data — every record here is
invented for demo purposes, in line with the hackathon's Data Usage Rules (synthetic /
anonymized data only). All coded tools in this agent network import from this module so
every agent reasons over the same consistent, live, in-memory "company" state.
"""

from __future__ import annotations
from typing import Dict, List, Any

# ---------------------------------------------------------------------------
# Bench associates: verified skills come from actual project/ticket history;
# official_skills is the stale, self-reported profile most matching tools miss.
# ---------------------------------------------------------------------------
BENCH_PEOPLE: List[Dict[str, Any]] = [
    {"id": "p1", "eid": "100101", "name": "Priya N.", "level": 4, "loc": "Chennai",
     "bench_days": 52, "official_skills": ["Angular", "Java"],
     "verified_skills": ["React", "AWS", "Node.js"]},
    {"id": "p2", "eid": "100102", "name": "Marcus T.", "level": 4, "loc": "Bangalore",
     "bench_days": 38, "official_skills": ["Java", "SQL"],
     "verified_skills": ["Java", "Spring Boot", "Kubernetes"]},
    {"id": "p3", "eid": "100103", "name": "Ananya R.", "level": 3, "loc": "Pune",
     "bench_days": 21, "official_skills": [".NET", "SQL"],
     "verified_skills": [".NET", "Azure", "SQL"]},
    {"id": "p4", "eid": "100104", "name": "Wei L.", "level": 5, "loc": "Hyderabad",
     "bench_days": 64, "official_skills": ["Python"],
     "verified_skills": ["Python", "Data Eng", "Snowflake", "AWS"]},
    {"id": "p5", "eid": "100105", "name": "Sofia M.", "level": 2, "loc": "Chennai",
     "bench_days": 19, "official_skills": ["SQL"],
     "verified_skills": ["SQL", "Python", "Data Eng"]},
    {"id": "p6", "eid": "100106", "name": "Omar F.", "level": 4, "loc": "Bangalore",
     "bench_days": 41, "official_skills": ["React", "Node.js", "Angular"],
     "verified_skills": ["React", "Node.js", "AWS"]},
    {"id": "p7", "eid": "100107", "name": "Karthik V.", "level": 3, "loc": "Bangalore",
     "bench_days": 33, "official_skills": ["Java"],
     "verified_skills": ["Java", "Spring Boot", "AWS"]},
    {"id": "p8", "eid": "100108", "name": "Neha S.", "level": 4, "loc": "Pune",
     "bench_days": 28, "official_skills": ["Manual QA"],
     "verified_skills": ["Salesforce", "SQL"]},
    {"id": "p9", "eid": "100109", "name": "Arjun M.", "level": 5, "loc": "Chennai",
     "bench_days": 47, "official_skills": ["Support"],
     "verified_skills": ["Kubernetes", "Terraform", "AWS"]},
    {"id": "p10", "eid": "100110", "name": "Divya P.", "level": 3, "loc": "Hyderabad",
     "bench_days": 24, "official_skills": [".NET"],
     "verified_skills": [".NET", "Azure", "SQL"]},
]

# ---------------------------------------------------------------------------
# New joiners: no project history yet — skills come from academy / capstone evidence.
# ---------------------------------------------------------------------------
NEW_JOINERS: List[Dict[str, Any]] = [
    {"id": "n1", "eid": "100201", "name": "Dev K.", "level": 1, "loc": "Chennai",
     "track": "Cloud Engineering", "cert": "AWS CCP", "joined_days": 18,
     "verified_skills": ["AWS", "Python", "Terraform"]},
    {"id": "n2", "eid": "100202", "name": "Lena H.", "level": 1, "loc": "Pune",
     "track": "Full-Stack", "cert": None, "joined_days": 12,
     "verified_skills": ["React", "Node.js", "SQL"]},
    {"id": "n3", "eid": "100203", "name": "Raj P.", "level": 1, "loc": "Bangalore",
     "track": "Java Microservices", "cert": None, "joined_days": 9,
     "verified_skills": ["Java", "Spring Boot", "SQL"]},
    {"id": "n4", "eid": "100204", "name": "Mei C.", "level": 2, "loc": "Hyderabad",
     "track": "Data Engineering", "cert": "SnowPro", "joined_days": 26,
     "verified_skills": ["Python", "SQL", "Snowflake"]},
    {"id": "n5", "eid": "100205", "name": "Tomas V.", "level": 1, "loc": "Chennai",
     "track": "Salesforce", "cert": None, "joined_days": 7,
     "verified_skills": ["Salesforce", "SQL"]},
]

# ---------------------------------------------------------------------------
# Shadow bench: appear 100% allocated everywhere, but logged hours reveal idle time.
# ---------------------------------------------------------------------------
SHADOW_BENCH: List[Dict[str, Any]] = [
    {"id": "s1", "name": "Hana S.", "level": 4, "loc": "Bangalore", "project": "Atlas",
     "phase": "maintenance", "logged_hrs": 10, "expected_hrs": 40,
     "verified_skills": ["React", "Node.js", "AWS"], "mgr_eid": "100303", "shadow_days": 392},
    {"id": "s2", "name": "Carlos D.", "level": 5, "loc": "Chennai", "project": "Orion",
     "phase": "ramp-down", "logged_hrs": 12, "expected_hrs": 40,
     "verified_skills": ["Java", "Kubernetes", "Terraform"], "mgr_eid": "100302", "shadow_days": 411},
    {"id": "s3", "name": "Yuki N.", "level": 3, "loc": "Pune", "project": "Helios",
     "phase": "slow phase", "logged_hrs": 16, "expected_hrs": 40,
     "verified_skills": ["Azure", ".NET", "SQL"], "mgr_eid": "100305", "shadow_days": 300},
    {"id": "s4", "name": "Aria B.", "level": 4, "loc": "Hyderabad", "project": "Nova",
     "phase": "post go-live", "logged_hrs": 8, "expected_hrs": 40,
     "verified_skills": ["Salesforce", "SQL"], "mgr_eid": "100307", "shadow_days": 372},
]

MANAGERS: List[Dict[str, Any]] = [
    {"eid": "100301", "name": "David M."}, {"eid": "100302", "name": "Sandra P."},
    {"eid": "100303", "name": "Hiro T."}, {"eid": "100304", "name": "Grace O."},
    {"eid": "100305", "name": "Vikram R."}, {"eid": "100306", "name": "Elena F."},
    {"eid": "100307", "name": "Tom B."}, {"eid": "100308", "name": "Nadia K."},
    {"eid": "100309", "name": "Leo M."}, {"eid": "100310", "name": "Priscilla J."},
]

# ---------------------------------------------------------------------------
# Open requisitions company-wide.
# ---------------------------------------------------------------------------
REQUISITIONS: List[Dict[str, Any]] = [
    {"id": "r1", "role": "Senior React Engineer", "client": "Meridian Bank", "level": 4,
     "loc": "Bangalore", "fresher_ok": False, "owner_eid": "100301", "skills": ["React", "AWS", "Node.js"]},
    {"id": "r2", "role": "Java Microservices Dev", "client": "Vertex Retail", "level": 4,
     "loc": "Bangalore", "fresher_ok": False, "owner_eid": "100310", "skills": ["Java", "Spring Boot", "Kubernetes"]},
    {"id": "r3", "role": "Cloud Engineer", "client": "Internal Platform", "level": 1,
     "loc": "Chennai", "fresher_ok": True, "owner_eid": "100307", "skills": ["AWS", "Terraform", "Python"]},
    {"id": "r4", "role": "Data Engineer", "client": "Lumen Health", "level": 4,
     "loc": "Hyderabad", "fresher_ok": False, "owner_eid": "100303", "skills": ["Python", "Snowflake", "Data Eng"]},
    {"id": "r5", "role": ".NET / Azure Developer", "client": "Nordic Logistics", "level": 3,
     "loc": "Pune", "fresher_ok": False, "owner_eid": "100304", "skills": [".NET", "Azure", "SQL"]},
    {"id": "r6", "role": "Full-Stack Developer", "client": "BrightEdu", "level": 2,
     "loc": "Pune", "fresher_ok": True, "owner_eid": "100308", "skills": ["React", "Node.js", "SQL"]},
    {"id": "r7", "role": "Salesforce Consultant", "client": "Cirrus CRM", "level": 4,
     "loc": "Hyderabad", "fresher_ok": False, "owner_eid": "100305", "skills": ["Salesforce", "SQL"]},
    {"id": "r8", "role": "DevOps / Kubernetes Eng.", "client": "Apex Media", "level": 5,
     "loc": "Chennai", "fresher_ok": False, "owner_eid": "100302", "skills": ["Kubernetes", "Terraform", "AWS"]},
    {"id": "r9", "role": "Senior Java Architect", "client": "Stronghold Insurance", "level": 5,
     "loc": "Bangalore", "fresher_ok": False, "owner_eid": "100309", "skills": ["Java", "Spring Boot", "AWS"]},
    {"id": "r10", "role": "SAP S/4HANA Consultant", "client": "Helios Manufacturing", "level": 4,
     "loc": "Pune", "fresher_ok": False, "owner_eid": "100306", "skills": ["SAP S/4HANA", "ABAP", "SQL"]},
]

# ---------------------------------------------------------------------------
# Free-text evidence used by the Skill Verification agent (project/ticket history).
# ---------------------------------------------------------------------------
EVIDENCE: Dict[str, str] = {
    "p1": "Led the front-end rebuild of a client portal using React + Redux; built REST integrations to "
          "Node.js services; deployed via AWS (S3, Lambda, CloudFront). Profile still says Angular/Java.",
    "p2": "Shipped a Spring Boot microservices platform, containerized with Docker, orchestrated on "
          "Kubernetes (Helm charts, HPA). Wrote the CI pipeline for the service.",
    "p4": "Built a Snowflake data warehouse and Airflow-orchestrated Python ETL jobs on AWS; the resume "
          "only lists 'Python' from three roles ago.",
    "p8": "Moved from manual QA into a Salesforce project: built Apex triggers, flows, and SQL-backed "
          "reports for a case-management org.",
}

# ---------------------------------------------------------------------------
# Blended hourly cost assumption for the savings ledger, shown transparently to users.
# ---------------------------------------------------------------------------
BLENDED_RATE_PER_HOUR = 1200  # INR

# ---------------------------------------------------------------------------
# Lookup helpers shared by every coded tool.
# ---------------------------------------------------------------------------

def all_bench_and_shadow() -> List[Dict[str, Any]]:
    return BENCH_PEOPLE + SHADOW_BENCH


def find_person(identifier: str) -> Dict[str, Any] | None:
    """Look up a person by id, employee id, or (case-insensitive) name fragment."""
    ident = str(identifier).strip().lower()
    for pool in (BENCH_PEOPLE, NEW_JOINERS, SHADOW_BENCH):
        for person in pool:
            if ident in (str(person.get("id", "")).lower(), str(person.get("eid", "")).lower()):
                return person
            if ident and ident in person["name"].lower():
                return person
    return None


def find_manager(eid: str) -> Dict[str, Any] | None:
    for m in MANAGERS:
        if m["eid"] == str(eid):
            return m
    return None


def find_requisition(identifier: str) -> Dict[str, Any] | None:
    ident = str(identifier).strip().lower()
    for r in REQUISITIONS:
        if ident in (r["id"].lower(), r["role"].lower(), r["client"].lower()):
            return r
    return None
