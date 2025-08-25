from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

DATABASE_URL = "sqlite:///./images.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SavedImage(Base):
    __tablename__ = "saved_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    photographer = Column(String, nullable=True)
    liked = Column(Boolean, default=False)
    saved = Column(Boolean, default=False)

def init_db():
    Base.metadata.create_all(bind=engine)
