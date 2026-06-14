import streamlit as st


def is_logged_in():

    return (
        "logged_in" in st.session_state
        and st.session_state.logged_in
    )


def get_current_user():

    if (
        "user" in st.session_state
        and st.session_state.user
    ):
        return st.session_state.user

    return None


def require_login():

    if not is_logged_in():

        st.warning(
            "Please login first."
        )

        st.session_state.page = "login"

        st.rerun()


def logout():

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "landing"

    st.rerun()