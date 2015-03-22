import os
import urlparse

import psycopg2


def create_connection():
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )


def run_sql(sql, params=(), fetch=False):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(sql, params)

    rows = []
    if fetch:
        rows = cursor.fetchall()
    else:
        conn.commit()

    cursor.close()
    conn.close()

    return rows


def create_messages_table():
    run_sql(
        """
        CREATE TABLE messages (id serial PRIMARY KEY, username text, message text);
        """
    )


def insert_message(username, message):
    username = username.encode('ascii', 'ignore')
    message = message.encode('ascii', 'ignore')

    run_sql(
        """
        INSERT INTO messages (username, message) VALUES (%s, %s);
        """,
        (username, message)
    )


def get_latest_messages():
    rows = run_sql(
        """
        SELECT * FROM messages ORDER BY id DESC LIMIT 15;
        """,
        fetch=True
    )

    return [
        {
            'id': r[0],
            'username': r[1],
            'text': r[2]
        } for r in rows
    ]
