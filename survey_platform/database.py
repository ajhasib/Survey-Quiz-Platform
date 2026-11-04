from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Database url
SQLALCHEMY_DATABASE_URL = "sqlite:///./survey_platform.db"

# Database Enginr
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
Base = declarative_base()

# Dependency to get database session
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
      db.close()
