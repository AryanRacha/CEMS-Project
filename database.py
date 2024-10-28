import sqlite3

# Function to create users table
def create_users_table():
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_event_table():
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            date TEXT,
            location TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_registration_table():
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            name TEXT,
            email TEXT,
            FOREIGN KEY(event_id) REFERENCES events(id)
        )
    """)
    conn.commit()
    conn.close()

# Function to add a new user
def add_user(name, email, username, password):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, email, username, password)
        VALUES (?, ?, ?, ?)
    """, (name, email, username, password))
    conn.commit()
    conn.close()

# Function to verify login credentials
def verify_user(username, password):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("""
        SELECT * FROM users WHERE username = ? AND password = ?
    """, (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_event(title, description, date, location):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO events (title, description, date, location) 
        VALUES (?, ?, ?, ?)
    """, (title, description, date, location))
    conn.commit()
    conn.close()

def get_all_events():
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()
    return events

def delete_event(event_id):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def register_user_for_event(event_id, name, email):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO registrations (event_id, name, email) 
        VALUES (?, ?, ?)
    """, (event_id, name, email))
    conn.commit()
    conn.close()

def get_participants_for_event(event_id):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("SELECT name, email FROM registrations WHERE event_id = ?", (event_id,))
    participants = c.fetchall()
    conn.close()
    return participants

def is_event_name_unique(title):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM events WHERE title = ?", (title,))
    result = c.fetchone()
    conn.close()
    return result[0] == 0  # True if the event name is unique

def already_registered(event_id, email):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    query = "SELECT COUNT(*) FROM registrations WHERE event_id = ? AND email = ?"
    c.execute(query, (event_id, email))
    count = c.fetchone()[0]
    return count > 0

def account_exists(username, email):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE username = ? OR email = ?", (username,email,))
    result = c.fetchone()
    conn.close()
    return result[0] == 0  # True if the event name is unique

# Function to get user information based on username
def get_user_info(username):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("SELECT name, email FROM users WHERE username = ?", (username,))
    user_info = c.fetchone()
    conn.close()
    return user_info

def registered_events(id):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    c.execute("SELECT * FROM events WHERE id = ?", (id,))
    participants = c.fetchall()
    conn.close()
    return participants

def fetch_events(search_query=None):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    if search_query:
        c.execute("SELECT id, title, description, date, location FROM events WHERE title LIKE ? OR description LIKE ?", 
                  ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        c.execute("SELECT id, title, description, date, location FROM events")
    events = c.fetchall()
    conn.close()
    return events

def registered_events(email):
    conn = sqlite3.connect("cems.db")
    c = conn.cursor()
    
    # Query to join events with registrations and filter by user name
    query = """
    SELECT e.id, e.title, e.description, e.date, e.location
    FROM events e
    JOIN registrations r ON e.id = r.event_id
    WHERE r.email = ?
    """
    
    c.execute(query, (email,))
    events = c.fetchall()
    
    conn.close()
    return events

def update_event(event_id, title, description, date, location):
    conn = sqlite3.connect('cems.db')
    c = conn.cursor()
    c.execute(
        """
        UPDATE events
        SET title = ?, description = ?, date = ?, location = ?
        WHERE id = ?
        """,
        (title, description, date, location, event_id)
    )
    conn.commit()
    conn.close()
