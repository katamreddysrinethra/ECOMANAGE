import streamlit as st

from database.db import (
    register_user,
    login_user
)


# ==========================================
# REGISTER PAGE
# ==========================================

def register_page():

    st.title("♻️ ECOMANAGE Registration")

    st.markdown(
        """
        Create your account to access ECOMANAGE.
        Citizens can request pickups and earn rewards.
        Collectors can manage and complete pickups.
        """
    )

    with st.form("register_form", clear_on_submit=False):

        st.subheader("User Information")

        name = st.text_input(
            "Full Name *"
        )

        email = st.text_input(
            "Email Address *"
        )

        phone = st.text_input(
            "Phone Number *"
        )

        role = st.selectbox(
            "Select Role *",
            [
                "Citizen",
                "Collector"
            ]
        )

        address = ""

        if role == "Citizen":

            address = st.text_area(
                "Address *"
            )

        st.subheader("Account Security")

        password = st.text_input(
            "Password *",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password *",
            type="password"
        )

        submit = st.form_submit_button(
            "Register"
        )

        if submit:

            # ----------------------
            # VALIDATIONS
            # ----------------------

            if not name.strip():

                st.error(
                    "Please enter your full name."
                )
                return

            if not email.strip():

                st.error(
                    "Please enter your email."
                )
                return

            if not phone.strip():

                st.error(
                    "Please enter your phone number."
                )
                return

            if role == "Citizen" and not address.strip():

                st.error(
                    "Please enter your address."
                )
                return

            if not password:

                st.error(
                    "Please enter a password."
                )
                return

            if len(password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )
                return

            if password != confirm_password:

                st.error(
                    "Passwords do not match."
                )
                return

            success = register_user(
                name=name,
                email=email,
                phone=phone,
                password=password,
                role=role,
                address=address
            )

            if success:

                st.success(
                    "Registration successful! Please login."
                )

                st.session_state.page = "login"

                st.rerun()

            else:

                st.error(
                    "An account with this email already exists."
                )

    st.write("")

    if st.button(
        "⬅ Back to Home",
        use_container_width=True
    ):

        st.session_state.page = "landing"

        st.rerun()


# ==========================================
# LOGIN PAGE
# ==========================================

def login_page():

    st.title("🔐 ECOMANAGE Login")

    st.markdown(
        """
        Login using your registered email and password.
        """
    )

    with st.form("login_form"):

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_button = st.form_submit_button(
            "Login"
        )

        if login_button:

            if not email.strip():

                st.error(
                    "Please enter your email."
                )
                return

            if not password:

                st.error(
                    "Please enter your password."
                )
                return

            user = login_user(
                email=email,
                password=password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.user = user

                if user["role"] == "Citizen":

                    st.session_state.page = "citizen"

                else:

                    st.session_state.page = "collector"

                st.success(
                    f"Welcome {user['name']}!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )

    st.write("")

    if st.button(
        "⬅ Back to Home",
        use_container_width=True
    ):

        st.session_state.page = "landing"

        st.rerun()


# ==========================================
# LOGOUT FUNCTION
# ==========================================

def logout():

    st.session_state.logged_in = False

    st.session_state.user = None

    st.session_state.page = "landing"

    st.rerun()