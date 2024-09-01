import asyncpg
from aiohttp import web

from app.config import Config
from app.handlers.handler import AuthHandler, NoteHandler


async def init_db() -> asyncpg.Pool:
    """Инициализация пула соединений с базой данных."""
    return await asyncpg.create_pool(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        host=Config.DB_HOST
    )


async def create_app() -> web.Application:
    """Создание и настройка веб-приложения."""
    app = web.Application()

    # Инициализация базы данных
    db_pool = await init_db()
    app['db'] = db_pool

    # Инициализация хендлеров
    auth_handler = AuthHandler(db_pool)
    note_handler = NoteHandler(db_pool)

    # Настройка роутеров
    app.router.add_post('/auth', auth_handler.login)
    app.router.add_post('/registry', auth_handler.register)
    app.router.add_post('/notes', note_handler.add_note)
    app.router.add_get('/notes', note_handler.get_notes)

    return app


if __name__ == '__main__':
    web.run_app(create_app())

