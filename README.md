 * CEMS Project Overview *

  -> Objective
     Develop an Event Management Website that allows users to view and register for events, while providing admins with tools to         manage events effectively.

-> Features

  1) User Interface
  -> Login/Register Users log in via a login page; a specific admin username and password are used for admin access.

  2) User View
  -> Event Listings: Displays events in boxes with title, description, date, location, and a "Register" button for user 
     registration (name, roll number, email).
  -> My Registrations: Users can view all events they registered for in a dedicated section.

#) Admin View
  -> Admin Login: Accessed with a specified admin username and password.
  -> Event Management: Admins can create, view, update, and delete events.
  -> View Participants: Admins can view the list of participants for each event.

-> Database Structure

  1) Database: SQLite
     Tables:
     events: Stores event details (title, description, date, location).
     registrations: Stores user registration data (name, roll number, email).

-> Team Members:

  Aryan Racha - 23102C0055
  Shreyas Gursale - 23102C0061
  Shruti Gupta - 23102C0051
  Sarah Cheulkar - 23102C0060
  Purvaj Gaonkar - 23102C0083
  Anish Murugaperumal - 23102C0076

-> Technologies Used
  App: Streamlit (Python)
  Database: SQLite (for CRUD operations)

-> Steps to run this project

Step 1 : Download the zip file
Step 2 : Extract the zip file
Step 3 : Open this file in cmd
Step 4 : Run this command ' pip install -r requirements.txt ' (This will install all the libraries for the project to run)
Step 5 : Next, run this command ' streamlit run app.py ' (This will run the website)
