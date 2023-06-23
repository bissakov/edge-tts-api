from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_path = r'D:\Work\tts-edge-api\app\database\text_to_speech.db'
engine = create_engine(f'sqlite:///{db_path}')

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
