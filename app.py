import streamlit as st

from database.db import create_tables

from pages.auth import (
    register_page,
    login_page
)

from pages.citizen_dashboard import citizen_dashboard
from pages.collector_dashboard import collector_dashboard


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="ECOMANAGE",
    page_icon="♻️",
    layout="wide"
)


# -----------------------------
# LOAD CSS
# -----------------------------

def load_css():

    try:
        with open(
            "assets/styles.css",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:
        pass


load_css()


# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------

create_tables()


# -----------------------------
# SESSION VARIABLES
# -----------------------------

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# -----------------------------
# LANDING PAGE
# -----------------------------

if st.session_state.page == "landing":

    st.markdown(
        """
        <div class='eco-title'>
        ♻️ ECOMANAGE
        </div>

        <div class='eco-subtitle'>
        Smart Waste Management Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.info(
        """
        Welcome to ECOMANAGE!

        Manage waste responsibly, request pickups,
        track environmental impact, earn rewards,
        and contribute towards a cleaner future.
        """
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "REGISTER",
            use_container_width=True
        ):
            st.session_state.page = "register"
            st.rerun()

        st.write("")

        if st.button(
            "LOGIN",
            use_container_width=True
        ):
            st.session_state.page = "login"
            st.rerun()


# -----------------------------
# REGISTER PAGE
# -----------------------------

elif st.session_state.page == "register":
    register_page()


# -----------------------------
# LOGIN PAGE
# -----------------------------

elif st.session_state.page == "login":
    login_page()


# -----------------------------
# CITIZEN INTERFACE
# -----------------------------

elif st.session_state.page == "citizen":

    if (
        not st.session_state.logged_in
        or st.session_state.user is None
    ):
        st.session_state.page = "login"
        st.rerun()

    citizen_dashboard()


# -----------------------------
# COLLECTOR INTERFACE
# -----------------------------

elif st.session_state.page == "collector":

    if (
        not st.session_state.logged_in
        or st.session_state.user is None
    ):
        st.session_state.page = "login"
        st.rerun()

    collector_dashboard()


# -----------------------------
# FALLBACK
# -----------------------------

else:

    st.session_state.page = "landing"
    st.rerun()