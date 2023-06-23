import edge_tts
from fastapi import APIRouter
from sqlalchemy import exc

from app.database.connection import Base, engine, session
from app.models.locale import LocaleTable
from app.models.voice import VoiceTable

router = APIRouter()


@router.post('/update_voices')
async def update_voices():
    list_voices = await edge_tts.list_voices()
    for voice_data in list_voices:
        try:
            locale = session.query(LocaleTable).filter_by(locale=voice_data['Locale']).first()
            if not locale:
                locale = LocaleTable(locale=voice_data['Locale'])
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


@router.post('/clean_list_voices')
async def clean_list_voices():
    session.query(VoiceTable).delete()
    session.commit()
    return {'message': 'Voices list cleaned'}


@router.get('/list_voices')
async def get_list_voices():
    voices = session.query(VoiceTable).all()
    voice_dicts = [voice.serialize() for voice in voices]
    return voice_dicts
