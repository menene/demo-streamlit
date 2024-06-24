import streamlit as st

# Sample list of users (dictionaries)
users = [
    {"name": "UVG", "email": "uvg", "password": "j204"},
]


def check_credentials(email, password):
    """Check if the provided email and password match any user in the list."""
    for user in users:
        if user["email"] == email and user["password"] == password:
            return True, user["name"]
    return False, None


def render_login_form():
    """Render the login form and handle login logic."""
    st.title("Login Page")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your passqword", type="password")
    login_button = st.button("Login")

    if login_button:
        valid, name = check_credentials(email, password)
        if valid:
            st.session_state.logged_in = True
            st.session_state.name = name
            st.rerun()
        else:
            st.error("Invalid email or password. Please try again.")


def display_dashboard():
    """Display the dashboard for logged-in users."""
    st.title("DASHBOARD")
    st.success(f"Welcome, {st.session_state.name}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.name = ""
        st.rerun()


# Initialize session state if not already initialized
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.name = ""

# Main logic
if st.session_state.logged_in:
    display_dashboard()
else:
    render_login_form()
