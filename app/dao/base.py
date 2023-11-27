"""Основной DAO (Data Access Object)"""
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker


class BaseDAO:
    """
    Основной DAO.
    Реализует основные CRUD-операции к модели
    """
    model = None

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        """Осуществляет поиск записи,
        удовлетворяющей переданным условиям

        Returns: объект модели либо None значение
        """
        session: AsyncSession
        async with async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **kwargs):
        """Поиск всех записей из модели

        Returns: список объектов модели
        """
        session: AsyncSession
        async with async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        """Добавление записи в таблицу
        """
        session: AsyncSession
        async with async_session_maker() as session:
            stmt = (
                insert(cls.model).
                values(**data)
            )
            await session.execute(stmt)
            await session.commit()
