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
            exit_time TEXT,
            persona_name TEXT
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

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS cafe_wait_times (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visitor_id INTEGER,
                    cafe_name TEXT,
                    arrival_time TEXT,
                    served_time TEXT,
                    prep_duration INTEGER,
                    wait_duration INTEGER,
                    FOREIGN KEY(visitor_id) REFERENCES visitors(id)
                )
                """)

        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS sport_wait_times (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        visitor_id INTEGER,
                        sport_name TEXT,
                        arrival_time TEXT,
                        start_time TEXT,
                        wait_duration INTEGER
                    )
                     """)

        conn.commit()


def log_entry(visitor_id, time_str,persona_name):
    with db_lock:
        with get_connection() as conn:
            conn.execute("""
                   INSERT OR IGNORE INTO visitors (id, entry_time, persona_name)
                   VALUES (?, ?, ?)
               """, (visitor_id, time_str, persona_name))
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

def log_cafe_wait_time(visitor_id, cafe_name, arrival_time, served_time, prep_duration, wait_duration):
    with db_lock:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO cafe_wait_times (
                    visitor_id, cafe_name, arrival_time, served_time,
                    prep_duration, wait_duration
                ) VALUES (?, ?,?, ?, ?, ?)
            """, (
                visitor_id, cafe_name,
                arrival_time.strftime("%H:%M:%S"),
                served_time.strftime("%H:%M:%S"),
                prep_duration, wait_duration
            ))
            conn.commit()

def log_sport_wait_time(visitor_id, sport_name, arrival_time, start_time, wait_duration):
    with db_lock:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO sport_wait_times (
                    visitor_id, sport_name, arrival_time, start_time, wait_duration
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                visitor_id,
                sport_name,
                arrival_time.strftime("%H:%M:%S"),
                start_time.strftime("%H:%M:%S"),
                wait_duration
            ))
            conn.commit()

def log_boat_wait_time(visitor_id, arrival_time, assigned_time, wait_duration):
    with db_lock:
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS boat_wait_times (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visitor_id INTEGER,
                    arrival_time TEXT,
                    assigned_time TEXT,
                    wait_duration INTEGER
                )
            """)
            conn.execute("""
                INSERT INTO boat_wait_times (
                    visitor_id, arrival_time, assigned_time, wait_duration
                ) VALUES (?, ?, ?, ?)
            """, (
                visitor_id,
                arrival_time.strftime("%H:%M:%S"),
                assigned_time.strftime("%H:%M:%S"),
                wait_duration
            ))
            conn.commit()

def log_bike_wait_time(visitor_id, arrival_time, assigned_time, wait_duration):
    with db_lock:
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bike_wait_times (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visitor_id INTEGER,
                    arrival_time TEXT,
                    assigned_time TEXT,
                    wait_duration INTEGER
                )
            """)
            conn.execute("""
                INSERT INTO bike_wait_times (
                    visitor_id, arrival_time, assigned_time, wait_duration
                ) VALUES (?, ?, ?, ?)
            """, (
                visitor_id,
                arrival_time.strftime("%H:%M:%S"),
                assigned_time.strftime("%H:%M:%S"),
                wait_duration
            ))
            conn.commit()
