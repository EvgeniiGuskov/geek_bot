from sqlalchemy import Integer, String, Column, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from ..declarative_base import Base


class Watches(Base):
    __tablename__ = "watches"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    timing = Column(String(255), nullable=False)
    kind = Column(String(255), nullable=False)
    general_score = Column(Numeric(2, 1), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    mustwatches = relationship("Mustwatches")


class Mustwatches(Base):
    __tablename__ = "mustwatches"

    id = Column(Integer, primary_key=True)
    user_score = Column(Integer, nullable=False)

    watch_id = Column(Integer, ForeignKey("watches.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
