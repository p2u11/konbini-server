from database import db
from sqlalchemy import select
from models import Banners

def get_banners() -> list:
    return [i.to_dict() for i in db.session.scalars(select(Banners)).all()]