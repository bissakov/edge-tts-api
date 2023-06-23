from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class LocaleTable(Base):
    __tablename__ = 'locales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    locale = Column(String, unique=True)

    voices = relationship('VoiceTable', back_populates='locale')

    def serialize(self):
        return {
            'id': self.id,
            'locale': self.locale,
        }
