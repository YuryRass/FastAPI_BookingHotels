"""Основной DAO (Data Access Object)"""
from sqlalchemy import CTE, delete, insert, select
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
        stmt = (
            insert(cls.model).
            values(**data).
            returning(cls.model.__table__.columns)
        )
        session: AsyncSession
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().all()

    @classmethod
    async def delete_records(cls, **kwargs):
        stmt = (
            delete(cls.model).
            filter_by(**kwargs).
            returning(cls.model.id)
        )

        session: AsyncSession
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().all()

    @staticmethod
    async def get_all(query: CTE, **kwargs):
        """Выводит все строки из CTE объекта по заданным критериям

        Args:
            query (CTE): SQL запрос представленный как:
        WITH ... AS (SELECT ...)
        """
        stmt = (
            select(query.columns).filter_by(**kwargs)
        )
        session: AsyncSession
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            return result.mappings().all()
