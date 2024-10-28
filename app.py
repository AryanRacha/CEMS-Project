import streamlit as st
import pandas as pd

from database import (
    create_event_table,
    create_registration_table,
    create_users_table,
    add_event,
    delete_event,
    register_user_for_event,
    get_participants_for_event,
    add_user,
    verify_user,
    is_event_name_unique,
    account_exists,
    get_user_info,
    already_registered,
    registered_events,
    fetch_events
)

# Initialize the database tables
create_users_table()
create_event_table()
create_registration_table()

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"  # Change this to a secure password in production

# Function for user login
def login():
    st.title("Event Management System")
    option = st.selectbox("Login/Sign-Up", ["Login", "Signup"])

    if option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["is_admin"] = True
                st.success("Logged in as Admin!")
                st.session_state["view"] = "admin"
                st.rerun()
            elif verify_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["is_admin"] = False
                st.session_state["username"] = username
                st.success("Logged in as User!")
                st.session_state["view"] = "user"
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    
    elif option == "Signup":
        return signup()
    
def signup():
    st.title("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        # Check if all fields are filled
        if not name.strip() or not email.strip() or not username.strip() or not password.strip():
            st.error("All fields (Name, Email, Username, Password) must be filled.")
        elif account_exists(username, email):
            add_user(name, email, username, password)
            st.success("Registration successful! You can now log in.")
            st.session_state["view"] = "login"
        else:
            st.error("This username and/or email already exists.")


# Function to handle logout
def logout():
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["view"] = "login"
        st.success("You have been logged out.")
        st.rerun()  # Reload the page to show the login screen

# Function to display the admin view
def admin_view():
    
    st.sidebar.title("Admin Menu")
    options = st.sidebar.radio("Select an action", ["Create Event", "Manage Events"])

    logout()

    if options == "Create Event":
        st.title("Create Event")
        title = st.text_input("Event Title")
        description = st.text_area("Event Description")
        date = st.date_input("Event Date")
        location = st.text_input("Event Location")

        if st.button("Add Event"):
        # Check if all fields are filled
            if not title.strip() or not description.strip() or not location.strip():
                st.error("All fields (Title, Description, Date, Location) must be filled.")
            elif is_event_name_unique(title):
                add_event(title, description, date.strftime("%Y-%m-%d"), location)
                st.success("Event added successfully!")
            else:
                st.error("An event with this title already exists. Please use a unique name.")

    elif options == "Manage Events":
        st.title("Manage Events")

        search_query = st.text_input("Search events by title or description", "")
        st.session_state.search_query = search_query  # Update session state
        st.write("")
        
        # Fetch events based on search query
        events = fetch_events(search_query if search_query.strip() else None)
        
        if events:
            for event in events:
                with st.container():
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                            <h4>{event[1]}</h4>
                            <p><strong>Description:</strong> {event[2]}</p>
                            <p><strong>Date:</strong> {event[3]}</p>
                            <p><strong>Location:</strong> {event[4]}</p>
                        </div>
                        """, unsafe_allow_html=True
                    )

                    col1, col2 = st.columns(2)

                    # View participants button
                    with col1:
                        if st.button("View Participants", key=f"participants_{event[0]}"):
                            participants = get_participants_for_event(event[0])
                            if participants:
                                st.subheader(f"Participants for {event[1]}")
                                participants_df = pd.DataFrame(participants, columns=["Name", "Email"])
                                st.table(participants_df)
                            else:
                                st.info("No participants have registered for this event.")

                    # Delete event button
                    with col2:
                        if st.button("Delete Event", key=f"delete_{event[0]}"):
                            delete_event(event[0])
                            st.success("Event deleted successfully!")
                            st.rerun()  # Refresh the list after deletion
        else:
            st.write("No events found.")

# Function to display the user view
def user_view():

    logout()

    user_info = get_user_info(st.session_state["username"])
    if not user_info:
        st.error("Error fetching user information.")
        return
    name, email = user_info  # Unpack user details

    st.sidebar.title("User Dashboard")
    choice = st.sidebar.radio("Go to", ["View Events", "Registered Events"])

    if choice == "View Events":
        st.title("Upcoming Events")

        search_query = st.text_input("Search events by title or description", "")
        st.session_state.search_query = search_query  # Update session state
        st.write("")
        
        # Fetch events based on search query
        events = fetch_events(search_query if search_query.strip() else None)

        if events:
            for event in events:
                with st.container():
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                            <h4>{event[1]}</h4>
                            <p><strong>Description:</strong> {event[2]}</p>
                            <p><strong>Date:</strong> {event[3]}</p>
                            <p><strong>Location:</strong> {event[4]}</p>
                        </div>
                        """, unsafe_allow_html=True
                    )

                    # Register for events
                    if st.button("Register", key=f"register_{event[0]}_unique"):
                        if already_registered(event[0],email):
                            st.warning("You have already registered for the event.")
                        else:
                            register_user_for_event(event[0], name, email)
                            st.success("Registration successful!")
                            
        else:
            st.write("No events found.")

    elif choice == "Registered Events":
        events = registered_events(email)
        for event in events:
            with st.container():
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                        <h4>{event[1]}</h4>
                        <p><strong>Description:</strong> {event[2]}</p>
                        <p><strong>Date:</strong> {event[3]}</p>
                        <p><strong>Location:</strong> {event[4]}</p>
                    </div>
                    """, unsafe_allow_html=True
                )


# Main application function
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["view"] = "login"

    if not st.session_state["logged_in"]:
        login()
    else:
        if st.session_state["is_admin"]:
            admin_view()
        else:
            user_view()

if __name__ == "__main__":
    main()