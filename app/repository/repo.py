import datetime
from typing import Optional, List, Dict, Any
import asyncpg


class UserRepository:
    def __init__(self, db: asyncpg.Pool) -> None:
        self.db = db

    async def get_user(self, login: str) -> Optional[asyncpg.Record]:
        """Получение пользователя по логину."""
        async with self.db.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM users WHERE login = $1", login)

    async def create_user(self, login: str, password: str) -> int:
        """Создание нового пользователя и возвращение его ID."""
        async with self.db.acquire() as conn:
            return await conn.fetchval(
                "INSERT INTO users (login, password) VALUES ($1, $2) RETURNING id",
                login,
                password
            )


class NoteRepository:
    def __init__(self, db: asyncpg.Pool) -> None:
        self.db = db

    async def create_note(self, user_id: int, content: str) -> int:
        """Создание новой заметки и возвращение её ID."""
        async with self.db.acquire() as conn:
            return await conn.fetchval(
                "INSERT INTO notes (user_id, content) VALUES ($1, $2) RETURNING id",
                user_id,
                content
            )

    async def get_notes(self, user_id: int) -> List[Dict[str, Any]]:
        """Получение всех заметок пользователя."""
        async with self.db.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM notes WHERE user_id = $1", user_id)
            return [
                dict(row, created_at=row['created_at'].isoformat() if isinstance(row['created_at'], datetime.datetime) else row['created_at'])
                for row in rows
            ]
