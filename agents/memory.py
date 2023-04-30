import sqlite3
import config

class DatabaseManager:
    def __init__(self):
        self.DATABASE_FILE = f"{config.DATABASE_DIRECTORY}/memory/memory.sqlite3"

    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.DATABASE_FILE)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return conn

    def close_connection(self, conn):
        try:
            if conn:
                conn.close()
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")

    def create_database(self):
        with self.connect() as conn:
            if not conn:
                print("Failed to create database")

    def get_database(self):
        conn = self.connect()
        if not conn:
            print("Failed to get database connection")
            return None
        return conn

    def create_tables(self):
        with self.get_database() as conn:
            if not conn:
                print("Failed to create tables")
                return
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS records
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          data TEXT,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            conn.commit()

    def insert_record(self, data):
        with self.get_database() as conn:
            if not conn:
                print("Failed to insert record")
                return
            c = conn.cursor()
            c.execute("INSERT INTO records (data) VALUES (?)", (data,))
            conn.commit()

    def retrieve_record(self, id):
        with self.get_database() as conn:
            if not conn:
                print("Failed to retrieve record")
                return
            c = conn.cursor()
            c.execute("SELECT * FROM records WHERE id=?", (id,))
            result = c.fetchone()
            return result

    def update_record(self, id, data):
        with self.get_database() as conn:
            if not conn:
                print("Failed to update record")
                return
            c = conn.cursor()
            c.execute("UPDATE records SET data=? WHERE id=?", (data, id))
            conn.commit()

    def delete_record(self, id):
        with self.get_database() as conn:
            if not conn:
                print("Failed to delete record")
                return
            c = conn.cursor()
            c.execute("DELETE FROM records WHERE id=?", (id,))
            conn.commit()

    def clear_cache(self):
        with self.get_database() as conn:
            if not conn:
                print("Failed to clear cache")
                return
            c = conn.cursor()
            c.execute("DELETE FROM records WHERE timestamp < datetime('now', '-1 day')")
            conn.commit()

    def get_last_chat_record(self):
        with self.get_database() as conn:
            if not conn:
                print("Failed to retrieve last chat record")
                return
            c = conn.cursor()
            c.execute("SELECT * FROM records ORDER BY id DESC LIMIT 1")
            result = c.fetchone()
            return result

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_database()
    db_manager.create_tables()
    db_manager.insert_record("test data")
    print(db_manager.retrieve_record(1))
    db_manager.update_record(1, "updated data")
    print(db_manager.retrieve_record(1))
    db_manager.delete_record(1)
    db_manager.clear_cache()
