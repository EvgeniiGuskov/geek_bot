from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from ..declarative_base import Base


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=False)

    users = relationship("Users")
    watches = relationship("Watches")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String(33), nullable=False)

    group_id = Column(Integer, ForeignKey("groups.id"))