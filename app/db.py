from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "sqlite:///./precioussteve.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread":False})

db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()