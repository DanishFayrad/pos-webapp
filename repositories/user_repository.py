from extensions import get_db


# 🔐 LOGIN — find by username
def find_user_by_username(username):
    conn = get_db()
    cur = conn.cursor()

    try:
        query = """
            SELECT user_id, branch_id, full_name, role, username, email, password
            FROM users
            WHERE username = %s
        """
        cur.execute(query, (username,))
        user = cur.fetchone()
        return user
    finally:
        cur.close()
        conn.close()


# 👤 CREATE USER
def create_user(branch_id, role, full_name, username, email, password):
    conn = get_db()
    cur = conn.cursor()

    try:
        query = """
            INSERT INTO users (branch_id, role, full_name, username, email, password)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING user_id;
        """

        cur.execute(query, (branch_id, role, full_name, username, email, password))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id

    finally:
        cur.close()
        conn.close()


# 📋 GET USERS
def get_users_by_branch(branch_id, is_admin=False):
    conn = get_db()
    cur = conn.cursor()

    try:
        if is_admin:
            query = """
                SELECT user_id, branch_id, full_name, role, username, email
                FROM users
            """
            cur.execute(query)
        else:
            query = """
                SELECT user_id, branch_id, full_name, role, username, email
                FROM users
                WHERE branch_id = %s
            """
            cur.execute(query, (branch_id,))

        users = cur.fetchall()
        return users

    finally:
        cur.close()
        conn.close()


# ✏️ UPDATE USER
def update_user(user_id, full_name, role):
    conn = get_db()
    cur = conn.cursor()

    try:
        query = """
            UPDATE users
            SET full_name = %s,
                role = %s
            WHERE user_id = %s
        """

        cur.execute(query, (full_name, role, user_id))
        conn.commit()

        return cur.rowcount  # ✅ tells if update happened

    finally:
        cur.close()
        conn.close()