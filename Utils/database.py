# Utils/database.py
import sqlite3
import threading

db_lock = threading.Lock()

def get_connection():
    return sqlite3.connect("retiro.db", check_same_thread=False)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Tabla de visitantes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY,
            entry_time TEXT,
            exit_time TEXT
        )
        """)
        # Tabla de actividades
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id INTEGER,
            activity_name TEXT,
            timestamp TEXT,
            FOREIGN KEY(visitor_id) REFERENCES visitors(id)
        )
        """)

        # Tabla de órdenes en cafés
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cafe_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id INTEGER,
            cafe_name TEXT,
            item_name TEXT,
            item_price REAL,
            FOREIGN KEY(visitor_id) REFERENCES visitors(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sport_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport_name TEXT NOT NULL,
            duration INTEGER NOT NULL,
            player_ids TEXT NOT NULL
        )
        """)

        conn.commit()


def log_entry(visitor_id, time_str):
    with db_lock:
        with get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO visitors (id, entry_time) VALUES (?, ?)", (visitor_id, time_str))
            conn.commit()

def log_exit(visitor_id, time_str):
    with db_lock:
        with get_connection() as conn:
            conn.execute("UPDATE visitors SET exit_time = ? WHERE id = ?", (time_str, visitor_id))
            conn.commit()

def log_activity(visitor_id, activity_name, time_str):
    with db_lock:
        with get_connection() as conn:
            conn.execute("INSERT INTO activities (visitor_id, activity_name, timestamp) VALUES (?, ?, ?)",
                         (visitor_id, activity_name, time_str))
            conn.commit()

def log_cafe_order(visitor_id, cafe_name, item_name, item_price):
    with db_lock:
        try:
            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO cafe_orders (visitor_id, cafe_name, item_name, item_price)
                    VALUES (?, ?, ?, ?)
                """, (visitor_id, cafe_name, item_name, item_price))
                conn.commit()
        except Exception as e:
            print(f"[DB ERROR] Failed to log cafe order for visitor {visitor_id}: {e}")


def log_sport_game(sport_name, duration, player_ids):
    with db_lock:
        try:
            player_ids_str = ",".join(map(str, player_ids))
            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO sport_games (sport_name, duration, player_ids)
                    VALUES (?, ?, ?)
                """, (sport_name, duration, player_ids_str))
                conn.commit()
        except Exception as e:
            print(f"[DB ERROR] Failed to log sport game '{sport_name}': {e}")
