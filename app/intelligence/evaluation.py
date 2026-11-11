def calculate_evaluation_metrics(
    verified_count: int,
    rejected_count: int,
    expected_count: int,
    execution_time: float,
):

    total = verified_count + rejected_count

    evidence_support_rate = (
        verified_count / total
        if total else 0
    )

    coverage = (
        verified_count / expected_count
        if expected_count else 0
    )

    return {
        "total_findings": total,
        "verified_findings": verified_count,
        "rejected_findings": rejected_count,

        "evidence_support_rate": round(
            evidence_support_rate,
            4,
        ),

        "coverage": round(
            min(coverage, 1.0),
            4,
        ),

        "unsupported_claim_rate": round(
            rejected_count / total if total else 0,
            4,
        ),

        "execution_time_seconds": round(
            execution_time,
            3,
        ),
    }