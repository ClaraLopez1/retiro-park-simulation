import sqlite3
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("example.db")
cursor = conn.cursor()
# Step 1: Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")
# Step 2: In ser t sample data
sample_users = [
("Alice", "alice@example.com"),
("Bob", "bob@example.com"),
("Charlie", "charlie@examp le.com")
]
cursor.executemany("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", sample_users)
# Com mit chan ges
conn.commit()
# Step 3: Qu ery an d pr int d ata
cursor .execute("SELECT * FROM users")
rows = cursor.fetchall()
print("Users in the database:")
for row in rows:
    print(row)
# Close the connection
conn.close()