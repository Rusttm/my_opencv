from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Router
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from AiogramPackage.TGAlchemy.TGModelProdSQLite import async_session


class DBMiddleware(BaseMiddleware):
    """ example middleware"""
    session_pool = None

    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            res_handler = await handler(event, data)
            return res_handler


router = Router()
router.message.middleware(DBMiddleware(session_pool=async_session))
