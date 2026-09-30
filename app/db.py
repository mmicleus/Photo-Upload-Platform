from collections.abc import AsyncGenerator
import uuid


from sqlalchemy import Column, String, Text, DateTime, ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from sqlalchemy.orm import DeclarativeBase, relationship

from datetime import datetime
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends


# URL to local database
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID,Base):
    posts = relationship("Post",back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    #randomly generates UUID for each post
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"),nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    fileType = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User",back_populates="posts")


engine = create_async_engine(DATABASE_URL)

aysnc_session_maker = async_sessionmaker(engine, expire_on_commit=False)



async def create_db_and_tables():
    #starts the engine
    async with engine.begin() as conn:
        #Finds all classes that inherit from DeclarativeBase and creates tables for them in the database
        await conn.run_sync(Base.metadata.create_all)


#allows us to start a session with the database and perform operations on it asynchronously. 
# The session is automatically closed after the operations are completed.
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with aysnc_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session,User)