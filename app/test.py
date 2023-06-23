from fastapi import FastAPI
import edge_tts
from sqlalchemy import ForeignKey, Integer, create_engine, Column, String, JSON, exc
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

db_path = r'/text_to_speech.db'
engine = create_engine(f'sqlite:///{db_path}')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class LocalesTable(Base):
    __tablename__ = 'locales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    locale = Column(String, unique=True)

    voices = relationship('VoiceTable', back_populates='locale')

    def serialize(self):
        return {
            'id': self.id,
            'locale': self.locale,
        }


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

    locale = relationship('LocalesTable', back_populates='voices')

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


Base.metadata.create_all(engine)

app = FastAPI()


@app.post('/update_voices')
async def update_voices():
    list_voices = await edge_tts.list_voices()
    for voice_data in list_voices:
        try:
            locale = session.query(LocalesTable).filter_by(locale=voice_data['Locale']).first()
            if not locale:
                locale = LocalesTable(locale=voice_data['Locale'])
                session.add(locale)
                session.commit()

            voice = VoiceTable(
                name=voice_data['Name'],
                short_name=voice_data['ShortName'],
                gender=voice_data['Gender'],
                locale=locale,  # Pass the locale instance
                suggested_codec=voice_data['SuggestedCodec'],
                friendly_name=voice_data['FriendlyName'],
                status=voice_data['Status']
            )
            session.add(voice)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
    return list_voices


@app.post('/clean_list_voices')
async def clean_list_voices():
    session.query(VoiceTable).delete()
    session.commit()
    return {'message': 'Voices list cleaned'}


@app.get('/list_voices')
async def get_list_voices():
    voices = session.query(VoiceTable).all()
    voice_dicts = [voice.serialize() for voice in voices]
    return voice_dicts


@app.get('/list_locales')
async def get_list_locales():
    locales = session.query(LocalesTable).all()
    locales_dict = [locale.serialize() for locale in locales]
    return locales_dict
