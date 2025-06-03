from sqlmodel import create_engine, Session, SQLModel

from ..settings import settings

# SQLModel setup
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
engine = create_engine(str(DATABASE_URL), echo=True)

# Create tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Database dependency
def get_session():
    with Session(engine) as session:
        yield session
