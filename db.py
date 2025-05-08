import mysql.connector
import datetime


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='personaltask'
    )

# ---------- USER OPERATIONS ----------

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                   (username, email, password))
    conn.commit()
    conn.close()

# ---------- TASK OPERATIONS ----------

def create_task(user_id, task_name, description, due_date, priority, category_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    created_date = datetime.date.today().isoformat()
    created_time = datetime.datetime.now().strftime('%H:%M')

    cursor.execute("""
        INSERT INTO tasks (task_name, description, created_date, created_time, due_date, priority, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (task_name, description, created_date, created_time, due_date, priority, category_id))

    task_id = cursor.lastrowid
    cursor.execute("INSERT INTO user_tasks (user_id, task_id) VALUES (%s, %s)", (user_id, task_id))
    conn.commit()
    conn.close()

def get_user_tasks(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.id, t.task_name, t.description, t.created_date as date, t.created_time as time,
               t.due_date as due, t.priority, c.category_name as category
        FROM tasks t
        LEFT JOIN categories c ON t.category_id = c.category_id
        JOIN user_tasks ut ON t.id = ut.task_id
        WHERE ut.user_id = %s
    """, (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(user_id, task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_tasks WHERE user_id = %s AND task_id = %s", (user_id, task_id))
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, task_name, description, due_date, priority, category_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks SET task_name = %s, description = %s, due_date = %s, priority = %s, category_id = %s
        WHERE id = %s
    """, (task_name, description, due_date, priority, category_id, task_id))
    conn.commit()
    conn.close()

# ---------- CATEGORY OPERATIONS ----------

def create_category(category_name, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (category_name, description) VALUES (%s, %s)", 
                   (category_name, description))
    conn.commit()
    conn.close()

def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def delete_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
    conn.commit()
    conn.close()

def update_category(category_id, category_name, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE categories SET category_name = %s, description = %s
        WHERE category_id = %s
    """, (category_name, description, category_id))
    conn.commit()
    conn.close()
