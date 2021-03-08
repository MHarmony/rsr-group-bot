from database.models.favorite import Favorite
from database.utils.base import Base, Engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        self.build()

    def build(self):
        Base.metadata.create_all(Engine, checkfirst=True)

        Session = sessionmaker(Engine)
        session = Session()

        try:
            Favorite()
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
