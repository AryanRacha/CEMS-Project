* CEMS Project Overview *

-> Team Members
Aryan Racha - 23102C0055
Shruti Gupta - 23102C0051
Shreyas Gursale - 23102C0061
Sarah Cheulkar - 23102C0060
Purvaj Gaonkar - 23102C0083

-> Project Objective

Developing an Event Management Website that facilitates users in viewing and registering for events while empowering an admin to manage these events efficiently through a straightforward web interface.

-> Features

1. User Interface

Initial Page:
Login/Register: Users access the website via a login page. A specific admin username and password are hardcoded for authentication. If the credentials match, the user gains admin access.

2. User View

Event Listings:
Users can view a list of all upcoming events displayed in a rectangular box format.
Each event box includes:
1> Title: The name of the event.
2> Description: A brief overview of what the event is about.
3> Date: The scheduled date of the event.
4> Location: Where the event will take place.
5> Register Button: Allows users to register for an event by submitting:
	a. Name
	b. Roll Number
	c. Email

My Registrations:
Users can view a separate list of all events they have registered for, enhancing their experience and organization.

3. Admin View

1> Admin Login: Admin can log in using a specified username and password.

2> Event Management:
	a. Create Events: Admin can input event details to add new events to the database.
	b. View Events: Admin can see a list of all available events, including their details.
	c. Update Events: Admin can edit existing event details (title, description, date, location) through an update form.
	d. Delete Events: Admin can remove events from the database by confirming the deletion action.

3> View Participants: For each event, the admin can see a list of participants who registered, allowing for effective event tracking.

-> Database Structure

Database: SQLite
Tables:
events: Stores event details (id, title, description, date, location).
registrations: Stores user registration details (user ID, event ID, name, roll number, email).

-> User Flow

The user lands on the login page.
If they are an admin, they enter the admin credentials to log in.
Regular users can view all events and register for any of them by submitting their details.
Admins can manage the event list by creating new events, updating event details, deleting events, and viewing participant lists.

-> Technology Stack

Frontend: Streamlit
Backend: SQLite (for database management)
