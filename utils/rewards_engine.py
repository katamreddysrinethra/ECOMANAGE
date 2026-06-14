def get_reward_points_for_waste(
        waste_type):

    reward_map = {

        "Plastic": 10,

        "Paper": 8,

        "Food": 5,

        "E-Waste": 20,

        "Glass": 12,

        "Metal": 15,

        "Hazardous": 25,

        "Other": 5
    }

    return reward_map.get(
        waste_type,
        5
    )


def get_badge(points):

    if points >= 300:
        return "🏆 Planet Protector"

    elif points >= 150:
        return "🥇 Sustainability Hero"

    elif points >= 50:
        return "🥈 Eco Warrior"

    else:
        return "🥉 Green Beginner"


def get_progress(points):

    target = 300

    progress = points / target

    return min(
        progress,
        1.0
    )