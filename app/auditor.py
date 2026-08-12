from __future__ import annotations

from app.measures import MEASURES
from app.models import AuditRequest, AuditResponse, AuditSummary, MeasureGap


class DocumentationAuditor:
    def audit(self, request: AuditRequest) -> AuditResponse:
        note = request.encounter_note.strip()
        passed: list[MeasureGap] = []
        gaps: list[MeasureGap] = []

        for measure in MEASURES:
            if request.encounter_type not in measure.applies_to:
                continue

            ok, finding, addendum = measure.check(note)
            item = MeasureGap(
                measure_id=measure.measure_id,
                measure_name=measure.name,
                category=measure.category,
                status="pass" if ok else "gap",
                finding=finding,
                suggested_addendum=None if ok else addendum,
            )
            if ok:
                passed.append(item)
            else:
                gaps.append(item)

        total = len(passed) + len(gaps)
        compliance = round(100 * len(passed) / total, 1) if total else 100.0

        return AuditResponse(
            summary=AuditSummary(
                total_measures=total,
                passed=len(passed),
                gaps=len(gaps),
                compliance_pct=compliance,
            ),
            gaps=gaps,
            passed=passed,
        )
