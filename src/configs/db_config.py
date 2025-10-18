from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from sqlalchemy.exc import OperationalError

Base = declarative_base()

class Database:
    _instance = None
    
    def __new__(cls, db_url: str = None):
        if cls._instance is None:
            if not db_url:
                raise ValueError("database URL is required")
            cls._instance = super(Database, cls).__new__(cls)
            connect_args = {}
            engine_kwargs = {
                "future": True,
                "pool_pre_ping": True,
                "pool_size": 10,
                "max_overflow": 20,
            }
            engine = create_engine(db_url, connect_args=connect_args, **engine_kwargs)
            cls._instance._engine = engine
            cls._instance._SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=cls._instance._engine, future=True
            )
        return cls._instance

    def get_db(self) -> Generator[Session, None, None]:
        db = self._SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def check_connection(self) -> bool:
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except OperationalError as e:
            raise Exception(f"database connection failed. err: {e}")
        except Exception as e:
            raise Exception(f"unexpected error while checking DB connection. err: {e}")
      
