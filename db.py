import os

from sqlalchemy import Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    tasks = relationship("Task")

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User('%s')>" % self.username


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    parent = relationship(User)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Task ('%s')>" % self.id

    def __str__(self):
        return "%s" % self.text


engine = create_engine(os.environ.get("DATABASE_URL"), echo=False)
Session = sessionmaker(bind=engine)
