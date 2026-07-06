from database import db
from models import App
from sqlalchemy import or_, select, and_

def api_app(app_id: int):
    app = db.session.scalars(select(App).where(App.id == app_id).limit(1)).all()
    return (app[0].to_dict(), 200) if app else ({}, 404)

def screenshots(app_id):
    app = api_app(app_id)
    return app[0]["screenshots"]

def versions(app_id):
    app = api_app(app_id)
    return app[0]["versions"]
