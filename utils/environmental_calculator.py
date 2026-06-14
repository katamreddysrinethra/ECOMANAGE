def calculate_carbon_saved(
        total_waste):

    return round(
        total_waste * 1.8,
        2
    )


def calculate_trees_saved(
        carbon_saved):

    return round(
        carbon_saved / 21,
        2
    )


def calculate_environmental_impact(
        total_waste):

    carbon_saved = calculate_carbon_saved(
        total_waste
    )

    trees_saved = calculate_trees_saved(
        carbon_saved
    )

    return {
        "total_waste": total_waste,
        "carbon_saved": carbon_saved,
        "trees_saved": trees_saved
    }