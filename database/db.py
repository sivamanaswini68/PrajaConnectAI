import os
import sqlite3
import uuid
from flask import g

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'prajaconnect.db')

def get_db():
    """Get thread-safe SQLite connection for current Flask request."""
    if 'db' not in g:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close SQLite connection at end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database tables and populate with rich seed data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT UNIQUE NOT NULL,
            name TEXT DEFAULT 'Citizen',
            age INTEGER DEFAULT 35,
            gender TEXT DEFAULT 'Other',
            state TEXT DEFAULT 'Andhra Pradesh',
            district TEXT DEFAULT 'Visakhapatnam',
            language TEXT DEFAULT 'English',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Schemes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            age_group TEXT DEFAULT 'All Ages',
            description TEXT NOT NULL,
            benefits TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            documents TEXT NOT NULL,
            how_to_apply TEXT NOT NULL,
            official_link TEXT NOT NULL,
            icon TEXT DEFAULT 'bi-award',
            is_demo INTEGER DEFAULT 1
        )
    ''')

    # Health Camps Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS camps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            camp_type TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            organizer TEXT NOT NULL,
            state TEXT DEFAULT 'Andhra Pradesh',
            district TEXT DEFAULT 'Visakhapatnam',
            location TEXT NOT NULL,
            latitude REAL DEFAULT 17.6868,
            longitude REAL DEFAULT 83.2185,
            age_group TEXT DEFAULT 'All Ages',
            contact TEXT NOT NULL,
            is_demo INTEGER DEFAULT 1
        )
    ''')

    # Applications Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            scheme_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Draft',
            submitted_date TEXT NOT NULL,
            notes TEXT DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (scheme_id) REFERENCES schemes (id)
        )
    ''')

    conn.commit()

    # Check if seed data exists; if empty, insert seed data
    cursor.execute("SELECT COUNT(*) FROM schemes")
    count = cursor.fetchone()[0]
    if count == 0:
        from database.seed_data import populate_seed_data
        populate_seed_data(conn)

    conn.close()

def get_or_create_user(user_uuid, name=None, age=None, gender=None, state=None, district=None, language=None):
    """Retrieve existing user or create a new user record safely."""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_uuid = ?", (user_uuid,))
    user = cursor.fetchone()
    
    if not user:
        new_uuid = user_uuid or str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO users (user_uuid, name, age, gender, state, district, language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_uuid,
                name or "Citizen",
                age or 35,
                gender or "Other",
                state or "Andhra Pradesh",
                district or "Visakhapatnam",
                language or "English"
            )
        )
        db.commit()
        cursor.execute("SELECT * FROM users WHERE user_uuid = ?", (new_uuid,))
        user = cursor.fetchone()
    return user
