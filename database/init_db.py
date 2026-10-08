from database.database import Base, engine
from database import models


def initialize_database():

    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully.")
    print(f"Database location: {engine.url}")


if __name__ == "__main__":
    initialize_database()