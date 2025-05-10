# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr
# from app.settings import Settings

# settings = Settings()

# engine = create_engine(
#     "postgresql+psycopg2://postgres:123@localhost:5433/pomodoro"
# )  # "sqlite:///pomodoro.sqlite"


# Session = sessionmaker(engine)


# def get_db_session() -> Session:
#     return Session

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.settings import Settings

settings = Settings()

engine = create_async_engine(url=settings.db_url, future=True, echo=True, pool_pre_ping=True)
AsyncSessionFactory = async_sessionmaker(engine,
                                         autoflush=False,
                                         expire_on_commit=False,
                                         )


# engine = create_engine(settings.db_url)
# Session = sessionmaker(bind=engine)


# async def get_db_session() -> AsyncSession:
#     async with AsyncSessionFactory() as session:
#         yield session

async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()