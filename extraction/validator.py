def validate_extraction(output):

    valid_claims = []

    for claim in output.claims:

        if not claim.subject:
            continue

        if not claim.object:
            continue

        if not claim.evidence.excerpt:
            continue

        valid_claims.append(claim)

    output.claims = valid_claims

    return output