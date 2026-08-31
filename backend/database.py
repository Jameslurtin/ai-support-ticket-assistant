import sqlite3

DB_NAME = "tickets.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            summary TEXT,
            suggested_action TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_ticket(
    title,
    description,
    status,
    category,
    priority,
    summary,
    suggested_action
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tickets (
            title,
            description,
            status,
            category,
            priority,
            summary,
            suggested_action
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            status,
            category,
            priority,
            summary,
            suggested_action
        )
    )

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()

    return ticket_id


def get_all_tickets():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            description,
            status,
            category,
            priority,
            summary,
            suggested_action
        FROM tickets
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows