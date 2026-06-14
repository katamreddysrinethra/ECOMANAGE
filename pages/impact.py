import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


DB_NAME = "ecomanage.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


# ==========================================
# ENVIRONMENTAL CALCULATIONS
# ==========================================

def calculate_carbon_saved(total_waste):

    return round(
        total_waste * 1.8,
        2
    )


def calculate_trees_saved(carbon_saved):

    return round(
        carbon_saved / 21,
        2
    )


# ==========================================
# MAIN PAGE
# ==========================================

def impact_page():

    st.title("🌍 Environmental Impact")

    st.info(
        """
        Track the positive environmental impact
        created through your completed waste
        recycling and disposal activities.
        """
    )

    user_id = st.session_state.user["id"]

    conn = get_connection()

    query = """
    SELECT
        waste_type,
        quantity
    FROM pickups
    WHERE citizen_id=?
    AND status='Completed'
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(user_id,)
    )

    conn.close()

    # ======================================
    # NO DATA
    # ======================================

    if df.empty:

        st.warning(
            """
            No completed pickups found.

            Complete waste pickups to generate
            environmental impact statistics.
            """
        )

        return

    # ======================================
    # HANDLE NULL VALUES
    # ======================================

    df["quantity"] = (
        df["quantity"]
        .fillna(0)
        .astype(float)
    )

    # ======================================
    # CALCULATIONS
    # ======================================

    total_waste = round(
        df["quantity"].sum(),
        2
    )

    carbon_saved = calculate_carbon_saved(
        total_waste
    )

    trees_saved = calculate_trees_saved(
        carbon_saved
    )

    completed_pickups = len(df)

    # ======================================
    # METRICS
    # ======================================

    st.subheader(
        "📊 Impact Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Completed Pickups",
            completed_pickups
        )

    with col2:

        st.metric(
            "Waste Recycled",
            f"{total_waste} kg"
        )

    with col3:

        st.metric(
            "CO₂ Saved",
            f"{carbon_saved} kg"
        )

    with col4:

        st.metric(
            "Trees Equivalent",
            trees_saved
        )

    st.divider()

    # ======================================
    # WASTE BREAKDOWN
    # ======================================

    st.subheader(
        "♻️ Waste Category Breakdown"
    )

    waste_summary = (
        df.groupby("waste_type")["quantity"]
        .sum()
        .reset_index()
    )

    waste_summary.columns = [
        "Waste Type",
        "Quantity"
    ]

    st.dataframe(
        waste_summary,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # PIE CHART
    # ======================================

    st.subheader(
        "🥧 Waste Distribution"
    )

    pie_chart = px.pie(
        waste_summary,
        names="Waste Type",
        values="Quantity",
        hole=0.3
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

    # ======================================
    # BAR CHART
    # ======================================

    st.subheader(
        "📈 Waste Collected by Category"
    )

    bar_chart = px.bar(
        waste_summary,
        x="Waste Type",
        y="Quantity",
        text_auto=True
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # ENVIRONMENTAL ACHIEVEMENTS
    # ======================================

    st.subheader(
        "🏆 Environmental Achievements"
    )

    if total_waste >= 500:

        st.success(
            "🏆 Planet Protector - 500kg+ recycled"
        )

    elif total_waste >= 250:

        st.success(
            "🥇 Sustainability Hero - 250kg+ recycled"
        )

    elif total_waste >= 100:

        st.success(
            "🥈 Eco Warrior - 100kg+ recycled"
        )

    else:

        st.info(
            "🥉 Green Beginner - Keep recycling!"
        )

    # ======================================
    # IMPACT MESSAGE
    # ======================================

    st.divider()

    st.subheader(
        "🌱 Your Contribution"
    )

    st.success(
        f"""
        Through responsible waste disposal,
        you have helped recycle {total_waste} kg
        of waste and potentially prevented
        approximately {carbon_saved} kg of CO₂
        emissions.

        Keep contributing towards a cleaner,
        greener and more sustainable future.
        """
    )

    # ======================================
    # ECO TIPS
    # ======================================

    st.divider()

    st.subheader(
        "💡 Ways to Increase Your Impact"
    )

    tips = [

        "Separate waste before disposal.",

        "Reduce single-use plastics.",

        "Recycle paper and cardboard.",

        "Dispose of e-waste responsibly.",

        "Compost food waste whenever possible.",

        "Encourage family members to recycle.",

        "Participate in community clean-up drives."
    ]

    for tip in tips:

        st.write(f"✅ {tip}")