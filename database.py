from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:#Tamrakar29@localhost/fastapi_crud_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
