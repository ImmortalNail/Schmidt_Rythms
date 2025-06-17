import aiosqlite
import datetime

db_path = "bot.db"

async def init_db():
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT,
            route TEXT,
            photo_path TEXT,
            created_at TEXT,
            photo_count INTEGER DEFAULT 0
        )''')
        await db.commit()

async def save_user(user_id, username, name):
    async with aiosqlite.connect(db_path) as db:
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        await db.execute("""
            INSERT OR REPLACE INTO users (user_id, username, name, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, name, now))
        await db.commit()

async def update_user_route(user_id, route):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE users SET route = ? WHERE user_id = ?", (route, user_id))
        await db.commit()

async def save_photo_path(user_id, path):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            UPDATE users
            SET photo_path = ?, photo_count = COALESCE(photo_count, 0) + 1
            WHERE user_id = ?
        """, (path, user_id))
        await db.commit()

async def get_all_users():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users")
        return await cursor.fetchall()

async def get_top_users():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT user_id FROM users ORDER BY photo_count DESC LIMIT 30")
        return [row[0] for row in await cursor.fetchall()]