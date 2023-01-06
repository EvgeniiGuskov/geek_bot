from sqlalchemy import Integer, String, Column, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship

from ..declarative_base import Base


class UserRequests(Base):
    __tablename__ = "user_requests"

    users_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    message_id = Column(String(33), nullable=True)
    add_or_delete = Column(Boolean, nullable=True)
    chosen_user_id = Column(String(33), nullable=True)
    add_or_take = Column(Boolean, nullable=True)
    title = Column(String(255), nullable=True)
    user_score = Column(Integer, nullable=True)


class Watches(Base):
    __tablename__ = "watches"

    title = Column(String(255), primary_key=True)
    general_score = Column(Numeric(2, 1), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    mustwatches = relationship("Mustwatches")


class Mustwatches(Base):
    __tablename__ = "mustwatches"

    id = Column(Integer, primary_key=True)
    user_score = Column(Integer, nullable=False)
    viewing_status = Column(Boolean, nullable=False)

    watch_title = Column(String(255), ForeignKey("watches.title"))
    user_id = Column(Integer, ForeignKey("users.id"))
