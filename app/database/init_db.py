from app.database.connection import Base, engine

from app.database.models import Competitor, ResearchPage


def initialize_database():

    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()