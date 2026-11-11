def compare_lists(
    previous: list[str],
    current: list[str],
):

    previous_set = set(previous)
    current_set = set(current)

    return {
        "added": sorted(current_set - previous_set),
        "removed": sorted(previous_set - current_set),
        "unchanged": sorted(previous_set & current_set),
    }

def compare_competitors(
    previous: dict,
    current: dict,
):

    categories = [
        "products",
        "target_customers",
        "value_propositions",
        "geographic_markets",
    ]

    changes = {}

    for category in categories:

        changes[category] = compare_lists(
            previous.get(category, []),
            current.get(category, []),
        )

    return changes