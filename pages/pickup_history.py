import streamlit as st
import pandas as pd

from database.db import (
    get_user_pickups,
    get_user_name
)


# ==========================================
# MAIN PAGE
# ==========================================

def pickup_history_page():

    st.title("📜 Pickup History")

    st.info(
        """
        Track all your pickup requests and monitor
        their current status.
        """
    )

    citizen_id = st.session_state.user["id"]

    pickups = get_user_pickups(
        citizen_id
    )

    if not pickups:

        st.info(
            "No pickup requests found."
        )
        return

    # ======================================
    # PROCESS DATA
    # ======================================

    records = []

    for pickup in pickups:

        pickup_id = pickup[0]
        waste_type = pickup[1]
        quantity = pickup[2]
        pickup_date = pickup[3]
        status = pickup[4]
        collector_id = pickup[5]

        image_path = ""
        notes = ""

        if len(pickup) > 6:
            image_path = pickup[6]

        if len(pickup) > 7:
            notes = pickup[7]

        collector_name = "Not Assigned"

        if collector_id:

            collector_name = get_user_name(
                collector_id
            )

        records.append(
            {
                "Pickup ID": pickup_id,
                "Waste Type": waste_type,
                "Quantity": quantity,
                "Pickup Date": pickup_date,
                "Status": status,
                "Collector": collector_name,
                "Image": image_path,
                "Notes": notes
            }
        )

    # ======================================
    # FILTER SECTION
    # ======================================

    st.subheader("🔍 Filter Requests")

    status_filter = st.selectbox(
        "Status",
        [
            "All",
            "Pending",
            "Accepted",
            "In Progress",
            "Completed"
        ]
    )

    filtered_records = records

    if status_filter != "All":

        filtered_records = [
            r for r in records
            if r["Status"] == status_filter
        ]

    # ======================================
    # STATISTICS
    # ======================================

    total = len(records)

    pending = len([
        r for r in records
        if r["Status"] == "Pending"
    ])

    accepted = len([
        r for r in records
        if r["Status"] == "Accepted"
    ])

    in_progress = len([
        r for r in records
        if r["Status"] == "In Progress"
    ])

    completed = len([
        r for r in records
        if r["Status"] == "Completed"
    ])

    st.subheader("📊 Pickup Statistics")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total",
            total
        )

    with col2:
        st.metric(
            "Pending",
            pending
        )

    with col3:
        st.metric(
            "Accepted",
            accepted
        )

    with col4:
        st.metric(
            "In Progress",
            in_progress
        )

    with col5:
        st.metric(
            "Completed",
            completed
        )

    st.divider()

    # ======================================
    # TABLE VIEW
    # ======================================

    table_data = []

    for record in filtered_records:

        table_data.append(
            {
                "Pickup ID": record["Pickup ID"],
                "Waste Type": record["Waste Type"],
                "Quantity": record["Quantity"],
                "Pickup Date": record["Pickup Date"],
                "Status": record["Status"],
                "Collector": record["Collector"]
            }
        )

    df = pd.DataFrame(
        table_data
    )

    st.subheader("📋 Pickup Overview")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # DETAILED VIEW
    # ======================================

    st.subheader("📦 Pickup Details")

    for record in filtered_records:

        with st.expander(
            f"Pickup #{record['Pickup ID']} - {record['Waste Type']}"
        ):

            st.write(
                f"**Pickup ID:** {record['Pickup ID']}"
            )

            st.write(
                f"**Waste Type:** {record['Waste Type']}"
            )

            st.write(
                f"**Quantity:** {record['Quantity']} kg"
            )

            st.write(
                f"**Pickup Date:** {record['Pickup Date']}"
            )

            st.write(
                f"**Collector:** {record['Collector']}"
            )

            st.write(
                f"**Status:** {record['Status']}"
            )

            if record["Notes"]:

                st.write(
                    f"**Notes:** {record['Notes']}"
                )

            if record["Image"]:

                try:

                    st.image(
                        record["Image"],
                        width=300,
                        caption="Uploaded Waste Image"
                    )

                except Exception:

                    st.warning(
                        "Image could not be loaded."
                    )

            st.divider()

            status = record["Status"]

            if status == "Pending":

                st.warning(
                    "⏳ Waiting for a collector to accept the request."
                )

            elif status == "Accepted":

                st.info(
                    "🚛 A collector has accepted this pickup."
                )

            elif status == "In Progress":

                st.info(
                    "🔄 Pickup is currently being processed."
                )

            elif status == "Completed":

                st.success(
                    "✅ Pickup completed successfully."
                )

    # ======================================
    # SUMMARY MESSAGE
    # ======================================

    st.divider()

    st.success(
        f"""
        Total Requests: {total}

        Completed Requests: {completed}

        Thank you for contributing towards a cleaner
        and greener environment.
        """
    )