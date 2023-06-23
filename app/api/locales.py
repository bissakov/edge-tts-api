from fastapi import APIRouter
from app.database.connection import session
from app.models.locale import LocaleTable

router = APIRouter()


@router.get('/list_locales')
async def get_list_locales():
    locales = session.query(LocaleTable).all()
    locales_dict = [locale.serialize() for locale in locales]
    return locales_dict


@router.post('/clean_list_locales')
async def clean_list_locales():
    session.query(LocaleTable).delete()
    session.commit()
    return {'message': 'Locales list cleaned'}
