from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime,timezone
import uuid
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./polls.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Poll(Base):
    __tablename__ = "polls"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question = Column(String, nullable=False)
    options = Column(Text, nullable=False)  # JSON string of options
    created_at = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)
    created_by = Column(String, default="anonymous")
    
    votes = relationship("Vote", back_populates="poll", cascade="all, delete-orphan")
    
    def get_options_list(self):
        return json.loads(self.options)

class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(String, ForeignKey("polls.id", ondelete="CASCADE"), nullable=False)
    option_index = Column(Integer, nullable=False)
    voted_at = Column(DateTime, default=datetime.now(timezone.utc))
    voter_id = Column(String, default="anonymous")
    
    poll = relationship("Poll", back_populates="votes")
    
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

class PollLike(Base):
    __tablename__ = "poll_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(String, ForeignKey("polls.id", ondelete="CASCADE"), nullable=False)
    voter_id = Column(String, nullable=False)
    liked_at = Column(DateTime, default=datetime.utcnow)
    
    poll = relationship("Poll")
    
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()