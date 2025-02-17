from sqlalchemy import Column, ForeignKey, Integer, String, Text
from db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")

    articles = relationship("Article", back_populates="author", cascade="all, delete")



class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, primary_key=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE",), nullable=False)

    author = relationship("User", back_populates="articles")