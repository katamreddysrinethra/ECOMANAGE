```python
import sqlite3
import bcrypt


DB_NAME = "ecomanage.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    conn = sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

    return conn


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------
    # USERS
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        address TEXT
    )
    """)

    # --------------------------
    # PICKUPS
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pickups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        citizen_id INTEGER NOT NULL,

        collector_id INTEGER,

        waste_type TEXT NOT NULL,

        quantity REAL DEFAULT 0,

        notes TEXT,

        pickup_date TEXT NOT NULL,

        image_path TEXT,

        status TEXT DEFAULT 'Pending',

        FOREIGN KEY (citizen_id)
        REFERENCES users(id),

        FOREIGN KEY (collector_id)
        REFERENCES users(id)
    )
    """)

    # --------------------------
    # REWARDS
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rewards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        points INTEGER DEFAULT 0,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    # --------------------------
    # COMPLAINTS
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        title TEXT NOT NULL,

        description TEXT NOT NULL,

        status TEXT DEFAULT 'Open',

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    # --------------------------
    # RATINGS
    # --------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        collector_id INTEGER NOT NULL,

        citizen_id INTEGER NOT NULL,

        rating INTEGER NOT NULL,

        feedback TEXT,

        FOREIGN KEY(collector_id)
        REFERENCES users(id),

        FOREIGN KEY(citizen_id)
        REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# ==========================================
# AUTHENTICATION FUNCTIONS
# ==========================================

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
        """,
        (
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
        """,
        (
            user_id,
            0
        ))

        conn.commit()

        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()

        return False


def login_user(
        email,
        password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email=?
    """,
    (email,))

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


# ==========================================
# USER FUNCTIONS
# ==========================================

def get_user_name(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM users
    WHERE id=?
    """,
    (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return "Not Assigned"


def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE id=?
    """,
    (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user


# ==========================================
# PICKUP FUNCTIONS
# ==========================================

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
    """,
    (collector_id,))

    pickups = cursor.fetchall()

    conn.close()

    return pickups


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


# ==========================================
# REWARD FUNCTIONS
# ==========================================

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


def get_reward_points(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT points
    FROM rewards
    WHERE user_id=?
    """,
    (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return 0


# ==========================================
# COMPLAINT FUNCTIONS
# ==========================================

def add_complaint(
        user_id,
        title,
        description):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO complaints(
        user_id,
        title,
        description,
        status
    )
    VALUES(?,?,?,?)
    """,
    (
        user_id,
        title,
        description,
        "Open"
    ))

    conn.commit()
    conn.close()


def get_user_complaints(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        title,
        description,
        status
    FROM complaints
    WHERE user_id=?
    ORDER BY id DESC
    """,
    (user_id,))

    complaints = cursor.fetchall()

    conn.close()

    return complaints


# ==========================================
# RATING FUNCTIONS
# ==========================================

def add_rating(
        collector_id,
        citizen_id,
        rating,
        feedback):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ratings(
        collector_id,
        citizen_id,
        rating,
        feedback
    )
    VALUES(?,?,?,?)
    """,
    (
        collector_id,
        citizen_id,
        rating,
        feedback
    ))

    conn.commit()
    conn.close()


def get_collector_average_rating(
        collector_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(rating)
    FROM ratings
    WHERE collector_id=?
    """,
    (collector_id,))

    rating = cursor.fetchone()[0]

    conn.close()

    if rating is None:
        return 0

    return round(rating, 2)
```
