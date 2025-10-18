from configs.db_config import Database, Base
from configs.config import Config
from models.model import Patient, Provider, Location, Appointment

def main():
    db = Database(Config.get_db_url())
    Base.metadata.create_all(bind=db._engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    main()