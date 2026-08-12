from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable


@dataclass
class QualityMeasure:
    measure_id: str
    name: str
    category: str
    applies_to: tuple[str, ...]  # encounter types
    check: Callable[[str], tuple[bool, str, str | None]]  # passed, finding, addendum


def _has_any(text: str, patterns: list[str]) -> bool:
    lower = text.lower()
    return any(re.search(p, lower) for p in patterns)


MEASURES: list[QualityMeasure] = [
    QualityMeasure(
        "CMS122",
        "Diabetes: HbA1c Documented",
        "Chronic disease",
        ("office", "inpatient"),
        lambda t: (
            _has_any(t, [r"\ba1c\b", r"\bhba1c\b", r"hemoglobin a1c", r"glycated hemoglobin"]),
            "HbA1c value or recent result documented" if _has_any(t, [r"\ba1c\b", r"\bhba1c\b"]) else "No HbA1c documentation found for diabetic visit",
            "Addendum: Most recent HbA1c ___% (date ___). Discussed glycemic targets with patient.",
        ),
    ),
    QualityMeasure(
        "CMS165",
        "Hypertension: BP Follow-up Plan",
        "Chronic disease",
        ("office", "ed"),
        lambda t: (
            _has_any(t, [r"blood pressure", r"\bbp\b", r"\d{2,3}/\d{2,3}"]) and _has_any(t, [r"follow[- ]?up", r"recheck", r"return in", r"home bp", r"lifestyle", r"medication adjustment"]),
            "Blood pressure addressed with follow-up plan" if _has_any(t, [r"follow[- ]?up", r"recheck"]) else "Elevated BP noted without documented follow-up plan",
            "Addendum: BP today ___. Plan: recheck in ___ weeks; home BP log reviewed; medication/lifestyle changes discussed.",
        ),
    ),
    QualityMeasure(
        "CMS68",
        "Documentation of Current Medications",
        "Medication safety",
        ("office", "inpatient", "ed"),
        lambda t: (
            _has_any(t, [r"medication reconciliation", r"med rec", r"current medications", r"medication list reviewed", r"home medications"]),
            "Medication reconciliation or current med list documented" if _has_any(t, [r"medication reconciliation", r"med rec"]) else "No medication reconciliation documentation",
            "Addendum: Medication reconciliation performed. Home medications reviewed with patient; discrepancies resolved.",
        ),
    ),
    QualityMeasure(
        "CMS2",
        "Depression Screening Follow-up",
        "Behavioral health",
        ("office",),
        lambda t: (
            not _has_any(t, [r"phq-?9", r"depression screen", r"depression screening"]) or _has_any(t, [r"phq-?9.*\d", r"screen negative", r"screen positive", r"counseling", r"referral", r"safety plan"]),
            "Depression screen with documented follow-up when screened" if True else "Screen without follow-up",
            "Addendum: PHQ-9 score ___. Result discussed; follow-up plan: ___ (counseling / referral / safety assessment as indicated).",
        ),
    ),
    QualityMeasure(
        "CMS69",
        "BMI Documented with Follow-up",
        "Preventive",
        ("office",),
        lambda t: (
            _has_any(t, [r"\bbmi\b", r"body mass index"]) and (
                not _has_any(t, [r"bmi.*(3[0-9]|[4-9]\d)"]) or _has_any(t, [r"weight management", r"nutrition", r"diet", r"exercise", r"bariatric", r"counseling"])
            ),
            "BMI documented with counseling when elevated" if _has_any(t, [r"\bbmi\b"]) else "BMI not documented",
            "Addendum: BMI ___ kg/m². Discussed nutrition and physical activity goals; referral to ___ as appropriate.",
        ),
    ),
    QualityMeasure(
        "CMS156",
        "Use of High-Risk Medications in Elderly",
        "Medication safety",
        ("office", "inpatient"),
        lambda t: (
            not _has_any(t, [r"\bbenzo", r"diazepam", r"lorazepam", r"zolpidem", r"diphenhydramine.*sleep"]) or _has_any(t, [r"risk discussed", r"deprescrib", r"taper", r"alternative", r"falls risk"]),
            "High-risk sedative use addressed or not present" if True else "High-risk medication without risk discussion",
            "Addendum: High-risk medication ___ reviewed; falls/cognitive risks discussed. Plan: taper/alternative ___.",
        ),
    ),
    QualityMeasure(
        "HEDIS-CDC",
        "Diabetes: Nephropathy Monitoring",
        "Chronic disease",
        ("office",),
        lambda t: (
            not _has_any(t, [r"type 2 diabetes", r"type 1 diabetes", r"\bt2dm\b", r"\be11"]) or _has_any(t, [r"urine albumin", r"microalbumin", r"uacr", r"egfr", r"nephropathy", r"ace inhibitor", r"arb"]),
            "Diabetes nephropathy monitoring documented" if _has_any(t, [r"egfr", r"microalbumin"]) else "Diabetic patient without nephropathy monitoring documentation",
            "Addendum: UACR/urine microalbumin ___ (date ___). eGFR ___. ACE/ARB therapy reviewed.",
        ),
    ),
    QualityMeasure(
        "TJC-MS",
        "Smoking Cessation Counseling",
        "Preventive",
        ("office", "inpatient", "ed"),
        lambda t: (
            not _has_any(t, [r"current smoker", r"tobacco use: yes", r"smokes \d", r"pack-year"]) or _has_any(t, [r"cessation", r"quit", r"nicotine replacement", r"varenicline", r"counseling", r"referral to quitline"]),
            "Smoking status addressed with cessation counseling when positive" if True else "Smoker without cessation counseling",
            "Addendum: Tobacco use confirmed. Cessation counseling provided; pharmacotherapy ___; quitline referral offered.",
        ),
    ),
]
