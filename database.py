import sqlite3
from datetime import datetime
import threading

class TaskDatabase:
    _local = threading.local()

    def __init__(self, db_name='tasks.db'):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_name)
        return self._local.connection

    def get_cursor(self):
        return self.get_connection().cursor()

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            completed_at TIMESTAMP
        )
        ''')
        conn.commit()
        cursor.close()

    def add_task(self, user_id, description):
        now = datetime.now()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO tasks (user_id, description, status, created_at)
        VALUES (?, ?, ?, ?)
        ''', (user_id, description, 'pending', now))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def get_tasks(self, user_id):
        cursor = self.get_cursor()
        cursor.execute('SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at', (user_id,))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks

    def mark_task_done(self, task_id, user_id):
        now = datetime.now()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE tasks SET status = ?, completed_at = ?
        WHERE id = ? AND user_id = ?
        ''', ('completed', now, task_id, user_id))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows > 0

    def close(self):
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            del self._local.connection