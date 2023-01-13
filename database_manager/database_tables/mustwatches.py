from sqlalchemy import Integer, String, Column, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship

from database_manager.database_tables.base.declarative_base import Base


class UserRequests(Base):
    __tablename__ = "user_requests"

    users_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    message_id = Column(String(33), nullable=True)
    add_or_delete = Column(Boolean, nullable=True)
    chosen_user_id = Column(String(33), nullable=True)
    title = Column(String(255), nullable=True)
    user_score = Column(Integer, nullable=True)


class Watches(Base):
    __tablename__ = "watches"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    general_score = Column(Numeric(3, 1, asdecimal=False), nullable=True)

    group_id = Column(String(33), ForeignKey("groups.id"))

    mustwatches = relationship("Mustwatches")


class Mustwatches(Base):
    __tablename__ = "mustwatches"

    id = Column(Integer, primary_key=True)
    user_score = Column(Integer, nullable=True)

    watches_id = Column(Integer, ForeignKey("watches.id"))
    users_id = Column(Integer, ForeignKey("users.id"))
