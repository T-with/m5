# Fixed version 2.2.0 - Added password field for freelancers
# This file has been updated to fix the database bugs
import os, sqlite3
from contextlib import contextmanager
from typing import Generator
from app.config import settings

DB_PATH = os.getenv('DATABASE_PATH', 'free_recruitment_market.db')

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Database connection context manager with improved locking

    Yields:
        sqlite3.Connection: Database connection with row factory
    """
    conn = sqlite3.connect(settings.db_path, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=30000')  # 30 seconds timeout
    try:
        yield conn
    finally:
        conn.close()


def init_database() -> None:
    """
    Initialize database tables for Free Recruitment Market

    Creates:
        - freelancers table (Job seeker)
        - evaluators table (Reviewer/Employer)
        - ratings table (Evaluation Record)
        - messages table (Direct messages between users)
        - listings table (Freelancer service listings)
        - booking_requests table (Client booking requests)
        - notifications table (System notifications)
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Drop old tables and recreate with new structure
        cursor.execute('DROP TABLE IF EXISTS message_attachments')
        cursor.execute('DROP TABLE IF EXISTS notifications')
        cursor.execute('DROP TABLE IF EXISTS booking_requests')
        cursor.execute('DROP TABLE IF EXISTS messages')
        cursor.execute('DROP TABLE IF EXISTS ratings')
        cursor.execute('DROP TABLE IF EXISTS evaluators')
        cursor.execute('DROP TABLE IF EXISTS freelancers')
        cursor.execute('DROP TABLE IF EXISTS listings')

        # Create freelancers table (Job Seeker Form - Extended Fields) with password
        cursor.execute('''
            CREATE TABLE freelancers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                phone TEXT,
                location TEXT,
                profile_picture TEXT,
                about_me TEXT,
                work_experience TEXT,
                skills TEXT,
                job_type TEXT,
                availability TEXT DEFAULT 'available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create evaluators table (Reviewer Table / Employer)
        cursor.execute('''
            CREATE TABLE evaluators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                company TEXT,
                position TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create ratings table (Reviewers evaluate job seekers)
        cursor.execute('''
            CREATE TABLE ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                freelancer_id INTEGER NOT NULL,
                evaluator_id INTEGER NOT NULL,
                rating INTEGER CHECK(rating >= 1 AND rating <= 5) NOT NULL,
                review_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE,
                FOREIGN KEY (evaluator_id) REFERENCES evaluators(id) ON DELETE CASCADE,
                UNIQUE(freelancer_id, evaluator_id)
            )
        ''')

        # Create messages table (direct messaging between job seekers and evaluators)
        cursor.execute('''
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                sender_role TEXT NOT NULL CHECK(sender_role IN ('job_seeker', 'evaluator')),
                sender_id INTEGER NOT NULL,
                receiver_role TEXT NOT NULL CHECK(receiver_role IN ('job_seeker', 'evaluator')),
                receiver_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create message_attachments table for storing file uploads tied to messages
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                mime_type TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            )
        ''')

        # Create listings table (Freelancer service listings)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                freelancer_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                base_price REAL NOT NULL,
                tags TEXT DEFAULT '[]',
                addons TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE
            )
        ''')

        # Create booking_requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS booking_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id INTEGER NOT NULL,
                freelancer_id INTEGER NOT NULL,
                client_role TEXT NOT NULL CHECK(client_role IN ('job_seeker', 'evaluator')),
                client_id INTEGER NOT NULL,
                client_name TEXT NOT NULL,
                requested_date TEXT NOT NULL,
                requested_time TEXT,
                location TEXT NOT NULL,
                description TEXT,
                selected_addons TEXT DEFAULT '[]',
                client_budget REAL,
                freelancer_price REAL,
                price_difference_percent REAL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'declined', 'in_progress', 'completed', 'cancelled')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
                FOREIGN KEY (freelancer_id) REFERENCES freelancers(id) ON DELETE CASCADE
            )
        ''')

        # Create notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_role TEXT NOT NULL CHECK(user_role IN ('job_seeker', 'evaluator')),
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                related_id INTEGER,
                related_type TEXT,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        print("✓ Database initialized successfully with all tables")
        print("✓ Freelancers table now includes password field")