import jwt
from aiohttp import web
from bcrypt import hashpw, gensalt, checkpw

import datetime
from functools import wraps
from typing import Callable, Awaitable, Dict, Any

from app.config import Config
from app.service.service import YandexSpellerService
from app.repository.repo import UserRepository, NoteRepository


def json_response(data: Dict[str, Any], status: int = 200) -> web.Response:
    return web.json_response(data, status=status)

# Проверка JWT токена 
def auth_required(handler: Callable[..., Awaitable[web.Response]]) -> Callable[..., Awaitable[web.Response]]:
    @wraps(handler)
    async def wrapped(self, request: web.Request, *args: Any, **kwargs: Any) -> web.Response:
        token: str = request.headers.get("Authorization", None)
        if not token:
            return json_response({"error": "Unauthorized"}, status=401)

        token = token.replace("Bearer ", "")
        try:
            payload: Dict[str, Any] = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
            request['user_id'] = payload['user_id']
        except jwt.ExpiredSignatureError:
            return json_response({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return json_response({"error": "Invalid token"}, status=401)

        return await handler(self, request, *args, **kwargs)
    
    return wrapped

# Базовый класс для хендлеров 
class BaseHandler:
    def __init__(self, db: Any) -> None:
        self.db = db

# Хендлеры для аутентификации 
class AuthHandler(BaseHandler):
    def __init__(self, db: Any) -> None:
        super().__init__(db)
        self.user_repo = UserRepository(db)

    async def login(self, request: web.Request) -> web.Response:
        data: Dict[str, Any] = await request.json()
        user: Dict[str, Any] = await self.user_repo.get_user(data['login'])

        if user and checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
            payload: Dict[str, Any] = {
                'user_id': user["id"],
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
            }
            token: str = jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
            return json_response({"token": token})
        
        return json_response({"error": "Invalid credentials"}, status=401)

    async def register(self, request: web.Request) -> web.Response:
        data: Dict[str, Any] = await request.json()
        hashed_password: str = hashpw(data['password'].encode('utf-8'), gensalt()).decode('utf-8')
        user_id: int = await self.user_repo.create_user(data['login'], hashed_password)
        return json_response({"user_id": user_id})

# Хендлеры для работы с заметками
class NoteHandler(BaseHandler):
    def __init__(self, db: Any) -> None:
        super().__init__(db)
        self.note_repo = NoteRepository(db)
        self.speller_service = YandexSpellerService()

    @auth_required
    async def add_note(self, request: web.Request) -> web.Response:
        user_id: int = request['user_id']
        data: Dict[str, Any] = await request.json()
        content: str = data.get("content", "")
        
        if len(content) > 1000 or len(content) == 0:
            return json_response({"error": "Note content too long or short"}, status=400)

        try:
            errors = await self.speller_service.check_spelling(content)
        except Exception as e:
            return json_response({"error": str(e)}, status=500)

        if errors:
            return json_response({"errors": errors}, status=400)

        note_id: int = await self.note_repo.create_note(user_id, content)
        return json_response({"note_id": note_id})

    @auth_required
    async def get_notes(self, request: web.Request) -> web.Response:
        user_id: int = request['user_id']
        notes: Dict[str, Any] = await self.note_repo.get_notes(user_id)
        return json_response({"notes": notes})
