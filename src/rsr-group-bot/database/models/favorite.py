from datetime import datetime
from uuid import uuid4

from database.utils.base import Base, Engine
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker


def defaultDate(context):
    return context.get_current_parameters()["date_added"]


class Favorite(Base):
    __tablename__ = "favorite"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    part_number = Column(String, unique=True)
    title = Column(String)
    price = Column(Float)
    available = Column(Integer, default=False)
    current = Column(Boolean, default=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=defaultDate, onupdate=datetime.utcnow)

    def __init__(self, partNumber=None, title=None, price=None, available=None, current=True):
        self.part_number = partNumber
        self.title = title
        self.price = price
        self.available = available
        self.current = current

    @staticmethod
    def add(favorites):
        Session = sessionmaker(Engine)
        session = Session()

        try:
            for favorite in favorites:
                session.add(favorite)

            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def get():
        Session = sessionmaker(Engine)
        session = Session()

        favorites = []

        try:
            favorites = session.query(Favorite).all()
        finally:
            session.close()

        return favorites

    @staticmethod
    def update(favorites):
        Session = sessionmaker(Engine)
        session = Session()

        try:
            session.bulk_update_mappings(Favorite, favorites)

            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
