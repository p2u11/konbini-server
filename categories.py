from database import db
from sqlalchemy import select

def get_categories(is_game=False, all=False) -> list[dict]:
    from models import Category
    return [dict(cat.to_dict()) for cat in db.session.scalars(select(Category) if all else (select(Category).where(Category.type == ("game" if is_game else "app")))).all()]

def get_category(category_id: str) -> dict | None:
    for i in get_categories(all=True):
        if i["code"] == category_id:
            return dict(i)
    return None