from database import db
from models import App
from sqlalchemy import or_, select, and_, cast, Integer

type_mapping = {"0": "app", "1": "game"}

def api_apps(q=None, is_game=None, category=None, limit=100, offset=0):
    stmt = select(App)
    
    if category: 
        stmt = stmt.where(App.category == category)

    if is_game in type_mapping:
        stmt = stmt.where(App.type == type_mapping[is_game])

    if q:
        search_param = f"%{q}%"
        stmt = stmt.where(
            or_(
                or_(
                    App.name.ilike(search_param),
                    App.package.ilike(search_param)
                ),
                App.tags.ilike(search_param)
            )
            
        )
    
    stmt = stmt.offset(offset).limit(limit)
    results = db.session.scalars(stmt).all()

    print(f"Found {len(results)} apps.") # Better logging
    return [dict(i.to_dict_short(), **{'rating':0.0,'downloads':12, 'review_count':9}) for i in results]

def api_apps_mobile(is_game='0', lang='en', device_api='1', q=None):
    stmt = select(App)

    if q:
        search_param = f"%{q}%"
        stmt = stmt.where(
            or_(
                App.name.ilike(search_param),
                App.package.ilike(search_param)
            )
        )
    
    if is_game == 1:
        stmt = stmt.where(App.type == "game")
    else:
        stmt = stmt.where(App.type == "app")

    stmt = stmt.where(cast(App.api, Integer) <= cast(device_api, Integer))
    
    stmt = stmt.limit(50)
    results = db.session.scalars(stmt).all()

    print(f"Found {len(results)} apps.") # Better logging
    return [dict(i.to_dict_short(), **{'rating':0.0,'downloads':12, 'review_count':9}) for i in results]

api_apps_search = api_apps

def get_apps_in_category(category: str):
    return {"category":category, "apps":api_apps(category=category)}

# TODO
def top_apps():
    return api_apps()