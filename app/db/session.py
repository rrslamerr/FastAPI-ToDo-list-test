from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_url)
Sessionlocal = sessionmaker(bind=engine)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
