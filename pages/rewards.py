import streamlit as st

from database.db import (
    get_reward_points
)


# ==========================================
# BADGE LOGIC
# ==========================================

def get_badge(points):

    if points >= 300:
        return "🏆 Planet Protector"

    elif points >= 150:
        return "🥇 Sustainability Hero"

    elif points >= 50:
        return "🥈 Eco Warrior"

    else:
        return "🥉 Green Beginner"


# ==========================================
# NEXT BADGE
# ==========================================

def next_badge_info(points):

    if points < 50:

        return (
            "🥈 Eco Warrior",
            50 - points,
            50
        )

    elif points < 150:

        return (
            "🥇 Sustainability Hero",
            150 - points,
            150
        )

    elif points < 300:

        return (
            "🏆 Planet Protector",
            300 - points,
            300
        )

    return (
        "Maximum Badge Achieved",
        0,
        300
    )


# ==========================================
# ACHIEVEMENTS
# ==========================================

def achievement_message(points):

    if points >= 300:

        return """
        🌍 Outstanding work!

        You are one of our top environmental
        contributors and have achieved the
        highest badge level.
        """

    elif points >= 150:

        return """
        🌱 Excellent contribution!

        Your recycling efforts are making
        a significant impact.
        """

    elif points >= 50:

        return """
        ♻️ Great progress!

        Keep submitting waste responsibly
        and continue earning rewards.
        """

    else:

        return """
        🌿 Welcome to ECOMANAGE!

        Start completing pickups to earn
        more reward points.
        """


# ==========================================
# MAIN PAGE
# ==========================================

def rewards_page():

    st.title("🎁 Rewards Center")

    st.info(
        """
        Earn eco-points by responsibly disposing
        of waste and completing pickup requests.
        """
    )

    user_id = st.session_state.user["id"]

    points = get_reward_points(
        user_id
    )

    badge = get_badge(
        points
    )

    next_badge, points_needed, target = (
        next_badge_info(points)
    )

    # ======================================
    # OVERVIEW
    # ======================================

    st.subheader(
        "🏅 Rewards Overview"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Reward Points",
            points
        )

    with col2:

        st.metric(
            "Current Badge",
            badge
        )

    st.divider()

    # ======================================
    # PROGRESS
    # ======================================

    st.subheader(
        "📈 Badge Progress"
    )

    if points < target:

        progress = points / target

        st.progress(
            min(progress, 1.0)
        )

        st.info(
            f"""
            {points_needed} more points needed
            to reach:

            {next_badge}
            """
        )

    else:

        st.progress(1.0)

        st.success(
            "Maximum badge achieved!"
        )

    st.divider()

    # ======================================
    # BADGE LEVELS
    # ======================================

    st.subheader(
        "🏆 Badge Levels"
    )

    st.success(
        """
        🥉 Green Beginner

        0 - 49 Points
        """
    )

    st.info(
        """
        🥈 Eco Warrior

        50 - 149 Points
        """
    )

    st.warning(
        """
        🥇 Sustainability Hero

        150 - 299 Points
        """
    )

    st.success(
        """
        🏆 Planet Protector

        300+ Points
        """
    )

    st.divider()

    # ======================================
    # REWARD SYSTEM
    # ======================================

    st.subheader(
        "♻️ Points Allocation"
    )

    reward_data = {
        "Plastic": 10,
        "Paper": 8,
        "Food": 5,
        "E-Waste": 20,
        "Glass": 12,
        "Metal": 15,
        "Hazardous": 25,
        "Other": 5
    }

    for waste, pts in reward_data.items():

        st.write(
            f"• {waste}: {pts} Points"
        )

    st.divider()

    # ======================================
    # IMPACT MESSAGE
    # ======================================

    st.subheader(
        "🌍 Achievement Status"
    )

    st.success(
        achievement_message(
            points
        )
    )

    st.divider()

    # ======================================
    # REWARD STATISTICS
    # ======================================

    st.subheader(
        "📊 Reward Statistics"
    )

    total_pickups_estimate = max(
        1,
        points // 10
    )

    avg_points = round(
        points / total_pickups_estimate,
        2
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Estimated Completed Pickups",
            total_pickups_estimate
        )

    with c2:

        st.metric(
            "Average Points Earned",
            avg_points
        )

    st.divider()

    # ======================================
    # TIPS
    # ======================================

    st.subheader(
        "💡 How to Earn More Points"
    )

    tips = [

        "Submit pickup requests regularly.",

        "Recycle hazardous waste responsibly.",

        "Dispose of e-waste through ECOMANAGE.",

        "Segregate waste properly before pickup.",

        "Encourage family members to recycle.",

        "Reduce contamination of recyclable waste."
    ]

    for tip in tips:

        st.write(
            f"✅ {tip}"
        )

    st.divider()

    st.success(
        f"""
        Current Points: {points}

        Current Badge: {badge}

        Keep contributing towards a cleaner
        and greener environment.
        """
    )