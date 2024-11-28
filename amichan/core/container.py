import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from amichan.core.config import get_app_settings
from amichan.core.settings.base import BaseAppSettings
from amichan.domain.mapper import IModelMapper
from amichan.domain.repositories.board import IBoardRepository
from amichan.domain.repositories.thread import IThreadRepository
from amichan.domain.services.board import IBoardService
from amichan.domain.services.thread import IThreadService
from amichan.infrastructure.mappers.board import BoardModelMapper
from amichan.infrastructure.mappers.thread import ThreadModelMapper
from amichan.infrastructure.repositories.board import BoardRepository
from amichan.infrastructure.repositories.thread import ThreadRepository
from amichan.services.board import BoardsService
from amichan.services.thread import ThreadService


class Container:
    """Dependency injector project container."""

    def __init__(self, settings: BaseAppSettings) -> None:
        self._settings = settings
        self._engine = create_async_engine(**settings.sqlalchemy_engine_props)
        self._session = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def context_session(self) -> AsyncIterator[AsyncSession]:
        session = self._session()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self._session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @staticmethod
    def thread_model_mapper() -> IModelMapper:
        return ThreadModelMapper()

    def thread_repository(self) -> IThreadRepository:
        return ThreadRepository(thread_mapper=self.thread_model_mapper())

    def thread_service(self) -> IThreadService:
        return ThreadService(
            thread_repo=self.thread_repository(),
        )

    @staticmethod
    def board_model_mapper() -> IModelMapper:
        return BoardModelMapper()

    def board_repository(self) -> IBoardRepository:
        return BoardRepository(board_mapper=self.board_model_mapper())

    def board_service(self) -> IBoardService:
        return BoardsService(
            board_repo=self.board_repository(),
        )


container = Container(settings=get_app_settings())
