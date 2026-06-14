import streamlit as st
import sqlite3
import pandas as pd


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
# SUBMIT COMPLAINT
# ==========================================

def submit_complaint(user_id):

    st.subheader("📝 Submit a Complaint")

    with st.form(
        "complaint_form",
        clear_on_submit=True
    ):

        title = st.text_input(
            "Complaint Title"
        )

        description = st.text_area(
            "Complaint Description"
        )

        submit = st.form_submit_button(
            "Submit Complaint"
        )

        if submit:

            if not title.strip():

                st.error(
                    "Please enter a complaint title."
                )
                return

            if not description.strip():

                st.error(
                    "Please enter complaint details."
                )
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO complaints(
                user_id,
                title,
                description,
                status
            )
            VALUES(?,?,?,?)
            """,
            (
                user_id,
                title.strip(),
                description.strip(),
                "Open"
            ))

            conn.commit()
            conn.close()

            st.success(
                "Complaint submitted successfully."
            )

            st.balloons()


# ==========================================
# COMPLAINT HISTORY
# ==========================================

def complaint_history(user_id):

    st.subheader(
        "📋 My Complaint History"
    )

    conn = get_connection()

    query = """
    SELECT
        id,
        title,
        description,
        status
    FROM complaints
    WHERE user_id=?
    ORDER BY id DESC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(user_id,)
    )

    conn.close()

    if df.empty:

        st.info(
            "You have not submitted any complaints yet."
        )

        return

    for _, row in df.iterrows():

        complaint_id = row["id"]
        title = row["title"]
        description = row["description"]
        status = row["status"]

        with st.expander(
            f"Complaint #{complaint_id} - {title}"
        ):

            st.write(
                f"**Complaint ID:** {complaint_id}"
            )

            st.write(
                f"**Title:** {title}"
            )

            st.write(
                f"**Description:**"
            )

            st.write(
                description
            )

            if status == "Open":

                st.warning(
                    "Status: Open"
                )

            elif status == "In Review":

                st.info(
                    "Status: In Review"
                )

            elif status == "Resolved":

                st.success(
                    "Status: Resolved"
                )

            else:

                st.write(
                    f"Status: {status}"
                )


# ==========================================
# COMPLAINT STATISTICS
# ==========================================

def complaint_statistics(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM complaints
    WHERE user_id=?
    """, (user_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM complaints
    WHERE user_id=?
    AND status='Open'
    """, (user_id,))

    open_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM complaints
    WHERE user_id=?
    AND status='Resolved'
    """, (user_id,))

    resolved_count = cursor.fetchone()[0]

    conn.close()

    st.subheader(
        "📊 Complaint Statistics"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Complaints",
            total
        )

    with col2:

        st.metric(
            "Open",
            open_count
        )

    with col3:

        st.metric(
            "Resolved",
            resolved_count
        )


# ==========================================
# MAIN PAGE
# ==========================================

def complaints_page():

    st.title("📢 Complaints & Support")

    st.info(
        """
        Submit complaints related to waste pickup,
        collector behavior, delays, missed pickups,
        or any other issue.
        """
    )

    user_id = st.session_state.user["id"]

    tab1, tab2 = st.tabs(
        [
            "Submit Complaint",
            "My Complaints"
        ]
    )

    with tab1:

        submit_complaint(
            user_id
        )

    with tab2:

        complaint_statistics(
            user_id
        )

        st.divider()

        complaint_history(
            user_id
        )