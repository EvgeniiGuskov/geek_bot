from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from ..declarative_base import Base


class Groups(Base):
    __tablename__ = "groups"

    id = Column(String(33), primary_key=True, autoincrement=False)

    users = relationship("Users")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(33), nullable=False)

    group_id = Column(String(33), ForeignKey("groups.id"))

    watches = relationship("Watches")
    mustwatches = relationship("Mustwatches")
