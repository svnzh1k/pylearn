from db.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship




class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, primary_key=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE",), nullable=False)

    author = relationship("User", back_populates="articles")