from sqlmodel import create_engine, Session, SQLModel


# SQLModel setup
DATABASE_URL = "sqlite:///./todo_app.db"
engine = create_engine(DATABASE_URL, echo=True)


# Create tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Database dependency
def get_session():
    with Session(engine) as session:
        yield session
