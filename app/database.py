import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_URL"]
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                message TEXT,
                project_need TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()


def add_lead(
    name,
    phone,
    email,
    message,
    project_need,
):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO leads (
            name,
            phone,
            email,
            message,
            project_need
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            phone,
            email,
            message,
            project_need,
        ),
    )

    db.commit()

    return cursor.lastrowid


def get_all_leads():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            phone,
            email,
            message,
            project_need,
            created_at
        FROM leads
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    return [dict(row) for row in rows]