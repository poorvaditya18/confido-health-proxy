from configs.db_config import Database
from configs.config import Config

db_instance: Database = None

def init_db():
    global db_instance
    if db_instance is None:
        db_instance = Database(Config.get_db_url())
    return db_instance

def get_db():
    db = db_instance.get_db()
    try:
        yield from db
    finally:
        pass