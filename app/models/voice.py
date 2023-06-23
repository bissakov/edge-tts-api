from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class VoiceTable(Base):
    __tablename__ = 'voices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    short_name = Column(String)
    gender = Column(String)
    locale_id = Column(Integer, ForeignKey('locales.id'))
    suggested_codec = Column(String)
    friendly_name = Column(String)
    status = Column(String)

    locale = relationship('LocaleTable', back_populates='voices')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'gender': self.gender,
            'locale': self.locale.locale,
            'suggested_codec': self.suggested_codec,
            'friendly_name': self.friendly_name,
            'status': self.status,
        }
