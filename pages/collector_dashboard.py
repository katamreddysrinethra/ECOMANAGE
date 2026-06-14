import streamlit as st
import pandas as pd

from database.db import (
    get_pending_pickups,
    get_collector_pickups,
    accept_pickup,
    update_pickup_status,
    get_pickup_details,
    add_reward_points
)
def collector_dashboard():

    st.title("♻️ Collector Dashboard")

    tab1, tab2, tab3 = st.tabs(
        [
            "Available Pickups",
            "My Pickups",
            "Statistics"
        ]
    )

    with tab1:
        available_pickups_tab()

    with tab2:
        my_pickups_tab()

    with tab3:
        statistics_tab()

# ==========================================
# REWARD CALCULATION
# ==========================================

def get_reward_points_for_waste(waste_type):

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


# ==========================================
# LOGOUT
# ==========================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "landing"

    st.rerun()


# ==========================================
# AVAILABLE PICKUPS
# ==========================================

def available_pickups_tab():

    st.subheader("📦 Available Pickup Requests")

    pickups = get_pending_pickups()

    if not pickups:

        st.success(
            "No pending pickup requests available."
        )

        return

    for pickup in pickups:

        pickup_id = pickup[0]
        citizen_id = pickup[1]
        waste_type = pickup[2]
        quantity = pickup[3]
        notes = pickup[4]
        pickup_date = pickup[5]
        image_path = pickup[6]
        status = pickup[7]

        with st.container():

            st.markdown("---")

            col1, col2 = st.columns([3, 1])

            with col1:

                st.markdown(
                    f"### ♻️ {waste_type}"
                )

                st.write(
                    f"**Pickup ID:** {pickup_id}"
                )

                st.write(
                    f"**Quantity:** {quantity} kg"
                )

                st.write(
                    f"**Pickup Date:** {pickup_date}"
                )

                st.write(
                    f"**Status:** {status}"
                )

                if notes:
                    st.write(
                        f"**Notes:** {notes}"
                    )

                if image_path:

                    try:
                        st.image(
                            image_path,
                            width=250
                        )

                    except Exception:
                        pass

            with col2:

                if st.button(
                    f"Accept Pickup #{pickup_id}",
                    key=f"accept_{pickup_id}"
                ):

                    accept_pickup(
                        pickup_id,
                        st.session_state.user["id"]
                    )

                    st.success(
                        "Pickup accepted successfully."
                    )

                    st.rerun()


# ==========================================
# MY PICKUPS
# ==========================================

def my_pickups_tab():

    st.subheader("🚛 My Assigned Pickups")

    collector_id = st.session_state.user["id"]

    pickups = get_collector_pickups(
        collector_id
    )

    if not pickups:

        st.info(
            "No pickups assigned yet."
        )

        return

    for pickup in pickups:

        pickup_id = pickup[0]
        waste_type = pickup[1]
        quantity = pickup[2]
        pickup_date = pickup[3]
        status = pickup[4]

        with st.expander(
            f"Pickup #{pickup_id} - {waste_type}"
        ):

            st.write(
                f"**Quantity:** {quantity} kg"
            )

            st.write(
                f"**Pickup Date:** {pickup_date}"
            )

            st.write(
                f"**Current Status:** {status}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Mark In Progress",
                    key=f"progress_{pickup_id}"
                ):

                    update_pickup_status(
                        pickup_id,
                        "In Progress"
                    )

                    st.success(
                        "Status updated successfully."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Mark Completed",
                    key=f"complete_{pickup_id}"
                ):

                    details = get_pickup_details(
                        pickup_id
                    )

                    citizen_id = details[0]
                    waste_type = details[1]

                    points = (
                        get_reward_points_for_waste(
                            waste_type
                        )
                    )

                    update_pickup_status(
                        pickup_id,
                        "Completed"
                    )

                    add_reward_points(
                        citizen_id,
                        points
                    )

                    st.success(
                        f"Pickup completed successfully. "
                        f"{points} reward points awarded."
                    )

                    st.balloons()

                    st.rerun()


# ==========================================
# STATISTICS TAB
# ==========================================

def statistics_tab():

    st.subheader(
        "📊 Collector Statistics"
    )

    collector_id = st.session_state.user["id"]

    pickups = get_collector_pickups(
        collector_id
    )

    total = len(pickups)

    accepted = len([
        p for p in pickups
        if p[4] == "Accepted"
    ])

    in_progress = len([
        p for p in pickups
        if p[4] == "In Progress"
    ])

    completed = len([
        p for p in pickups
        if p[4] == "Completed"
    ])

    completion_rate = 0

    if total > 0:

        completion_rate = round(
            (completed / total) * 100,
            2
        )
