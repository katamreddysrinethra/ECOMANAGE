import streamlit as st
import sqlite3

from streamlit_option_menu import option_menu

from pages.pickup_request import pickup_request_page
from pages.pickup_history import pickup_history_page
from pages.rewards import rewards_page
from pages.complaints import complaints_page
from pages.impact import impact_page
from pages.education_hub import education_hub_page


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
# DASHBOARD HOME
# ==========================================

def dashboard_home():

    user = st.session_state.user

    user_id = user["id"]

    conn = get_connection()
    cursor = conn.cursor()

    # Total pickups

    cursor.execute("""
    SELECT COUNT(*)
    FROM pickups
    WHERE citizen_id=?
    """, (user_id,))

    total_pickups = cursor.fetchone()[0]

    # Pending pickups

    cursor.execute("""
    SELECT COUNT(*)
    FROM pickups
    WHERE citizen_id=?
    AND status='Pending'
    """, (user_id,))

    pending_pickups = cursor.fetchone()[0]

    # Accepted pickups

    cursor.execute("""
    SELECT COUNT(*)
    FROM pickups
    WHERE citizen_id=?
    AND status='Accepted'
    """, (user_id,))

    accepted_pickups = cursor.fetchone()[0]

    # Completed pickups

    cursor.execute("""
    SELECT COUNT(*)
    FROM pickups
    WHERE citizen_id=?
    AND status='Completed'
    """, (user_id,))

    completed_pickups = cursor.fetchone()[0]

    # Reward points

    cursor.execute("""
    SELECT points
    FROM rewards
    WHERE user_id=?
    """, (user_id,))

    reward_row = cursor.fetchone()

    points = reward_row[0] if reward_row else 0

    conn.close()

    # =====================================
    # UI
    # =====================================

    st.title("♻️ Citizen Dashboard")

    st.success(
        f"Welcome back, {user['name']} 🌱"
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Pickups",
            total_pickups
        )

    with col2:
        st.metric(
            "Pending",
            pending_pickups
        )

    with col3:
        st.metric(
            "Accepted",
            accepted_pickups
        )

    with col4:
        st.metric(
            "Completed",
            completed_pickups
        )

    st.write("")

    st.metric(
        "Reward Points",
        points
    )

    st.divider()

    st.subheader("🌍 Your Contribution")

    st.info(
        """
        Every waste pickup contributes towards a cleaner,
        greener and healthier environment.
        Keep recycling and earn rewards while helping
        your community.
        """
    )

    st.divider()

    st.subheader("📋 Recent Activity")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        waste_type,
        pickup_date,
        status
    FROM pickups
    WHERE citizen_id=?
    ORDER BY id DESC
    LIMIT 5
    """, (user_id,))

    recent_activity = cursor.fetchall()

    conn.close()

    if recent_activity:

        for activity in recent_activity:

            waste_type = activity[0]
            pickup_date = activity[1]
            status = activity[2]

            if status == "Pending":

                st.warning(
                    f"{waste_type} | {pickup_date} | Pending"
                )

            elif status == "Accepted":

                st.info(
                    f"{waste_type} | {pickup_date} | Accepted"
                )

            elif status == "In Progress":

                st.info(
                    f"{waste_type} | {pickup_date} | In Progress"
                )

            elif status == "Completed":

                st.success(
                    f"{waste_type} | {pickup_date} | Completed"
                )

    else:

        st.info(
            "No activity available yet."
        )


# ==========================================
# LOGOUT
# ==========================================

def logout():

    st.session_state.logged_in = False

    st.session_state.user = None

    st.session_state.page = "landing"

    st.rerun()


# ==========================================
# MAIN DASHBOARD
# ==========================================

def citizen_dashboard():

    with st.sidebar:

        st.title("♻️ ECOMANAGE")

        st.write(
            f"👤 {st.session_state.user['name']}"
        )

        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Pickup Request",
                "Pickup History",
                "Rewards",
                "Complaints",
                "Environmental Impact",
                "Education Hub",
                "Logout"
            ],
            icons=[
                "house",
                "truck",
                "clock-history",
                "gift",
                "chat-left-text",
                "graph-up",
                "book",
                "box-arrow-right"
            ],
            default_index=0
        )

    # =====================================
    # PAGE ROUTING
    # =====================================

    if selected == "Dashboard":

        dashboard_home()

    elif selected == "Pickup Request":

        pickup_request_page()

    elif selected == "Pickup History":

        pickup_history_page()

    elif selected == "Rewards":

        rewards_page()

    elif selected == "Complaints":

        complaints_page()

    elif selected == "Environmental Impact":

        impact_page()

    elif selected == "Education Hub":

        education_hub_page()

    elif selected == "Logout":

        logout()