from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "postgresql://super_svnzh1k:123@localhost:5432/svnzh1k"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
    print("inited db")

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close() 