import sqlite3
import hashlib
import os
import binascii
import bcrypt

DB_NAME = "ecomanage.db"

def add_pickup_request(
        citizen_id,
        waste_type,
        quantity,
        notes,
        pickup_date,
        image_path):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO pickups(
        citizen_id,
        waste_type,
        quantity,
        notes,
        pickup_date,
        image_path,
        status
    )
    VALUES(?,?,?,?,?,?,?)
    """,
    (
        citizen_id,
        waste_type,
        quantity,
        notes,
        pickup_date,
        image_path,
        "Pending"
    ))

    conn.commit()
    conn.close()

def get_user_pickups(citizen_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        waste_type,
        quantity,
        pickup_date,
        status,
        collector_id,
        image_path,
        notes
    FROM pickups
    WHERE citizen_id=?
    ORDER BY id DESC
    """,
    (citizen_id,))

    pickups = cursor.fetchall()

    conn.close()

    return pickups
def get_user_name(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM users
    WHERE id=?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return "Not Assigned"
def get_reward_points(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT points
    FROM rewards
    WHERE user_id=?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return 0
def get_pending_pickups():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        citizen_id,
        waste_type,
        quantity,
        notes,
        pickup_date,
        image_path,
        status
    FROM pickups
    WHERE status='Pending'
    ORDER BY pickup_date ASC
    """)

    pickups = cursor.fetchall()

    conn.close()

    return pickups
def get_collector_pickups(collector_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        waste_type,
        quantity,
        pickup_date,
        status
    FROM pickups
    WHERE collector_id=?
    ORDER BY id DESC
    """, (collector_id,))

    pickups = cursor.fetchall()

    conn.close()

    return pickups
def accept_pickup(
        pickup_id,
        collector_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE pickups
    SET
        collector_id=?,
        status='Accepted'
    WHERE id=?
    """,
    (
        collector_id,
        pickup_id
    ))

    conn.commit()
    conn.close()
def update_pickup_status(
        pickup_id,
        status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE pickups
    SET status=?
    WHERE id=?
    """,
    (
        status,
        pickup_id
    ))

    conn.commit()
    conn.close()
def get_pickup_details(pickup_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        citizen_id,
        waste_type
    FROM pickups
    WHERE id=?
    """,
    (pickup_id,))

    data = cursor.fetchone()

    conn.close()

    return data
def add_reward_points(
        user_id,
        points):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE rewards
    SET points = points + ?
    WHERE user_id=?
    """,
    (
        points,
        user_id
    ))

    conn.commit()
    conn.close()            
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def hash_password(password):
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return binascii.hexlify(salt).decode() + '$' + binascii.hexlify(key).decode()


def verify_password(password, stored_password):
    try:
        salt_hex, key_hex = stored_password.split('$')
    except ValueError:
        return False
    salt = binascii.unhexlify(salt_hex)
    key = binascii.unhexlify(key_hex)
    verify_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hashlib.compare_digest(key, verify_key)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        address TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pickups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        citizen_id INTEGER,
        collector_id INTEGER,
        waste_type TEXT,
        quantity REAL,
        notes TEXT,
        pickup_date TEXT,
        image_path TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rewards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        points INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        status TEXT DEFAULT 'Open'
    )
    """)

    conn.commit()
    conn.close()


def register_user(
        name,
        email,
        phone,
        password,
        role,
        address):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute("""
        INSERT INTO users(
            name,
            email,
            phone,
            password,
            role,
            address
        )
        VALUES(?,?,?,?,?,?)
        """, (
            name,
            email,
            phone,
            hashed_password.decode(),
            role,
            address
        ))

        conn.commit()

        user_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO rewards(
            user_id,
            points
        )
        VALUES(?,?)
        """, (
            user_id,
            0
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email=?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    if not user:
        return None

    stored_password = user[4]

    if bcrypt.checkpw(
            password.encode(),
            stored_password.encode()):

        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "phone": user[3],
            "role": user[5],
            "address": user[6]
        }

    return None