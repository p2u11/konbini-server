# models.py
from database import db
import categories, json

class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.Text, nullable=False)
    package = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False, server_default=db.text("''"))
    icon = db.Column(db.Text, nullable=False, server_default=db.text("'no_icon.png'"))
    tags = db.Column(db.Text, nullable=False, server_default=db.text("''"))
    _screenshots = None
    screenshots = db.Column(db.Text, nullable=False, server_default=db.text("'[]'"))
    _versions = None
    versions = db.Column(db.Text, nullable=False, server_default=db.text("'[]'"))

    type = db.Column(db.Text)  # app/game

    # Dev console only, TODO
    uploaded = db.Column(db.Text)  # who uploaded the app (dev console, TODO)
    visible = db.Column(db.Integer, nullable=False, server_default=db.text("0")) # unverified apps
    first_date = db.Column(db.Integer, nullable=False, server_default=db.text("'[]'")) # upload date
    last_date = db.Column(db.Integer) # last updated

    def to_dict_short(self):
        cat_dict = categories.get_category(self.category)
        category_label = cat_dict["label"] if cat_dict else self.category
        """
        id: { type: integer }
        name: { type: string }
        category_code: { type: string }
        category_label: { type: string }
        rating: { type: number, format: float }
        downloads: { type: integer }
        review_count: { type: integer }
        apk_file: { type: string }
        """
        self._versions = self._versions if self._versions else json.loads(self.versions)
        if not self._versions:
            self._versions = [{"version":"n/a", "apk_file":"na.apk", "api":9999, "arch":"noarch"}]
        return {
            "id": self.id,
            "name": self.name,
            "category_code": self.category,
            "category_label": category_label,
            "apk_file": self._versions[0]["apk_file"],
            "icon": self.icon,
        }
    
    def to_dict(self):
        cat_dict = categories.get_category(self.category)
        category_label = cat_dict["label"] if cat_dict else self.category
        self._versions = self._versions if self._versions else json.loads(self.versions)
        if not self._versions:
            self._versions = [{"version":"n/a", "apk_file":"na.apk", "api":9999}]
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "category": self.category,
            "description": self.description,
            "version": self._versions[0]["version"],
            "apk_file": self._versions[0]["apk_file"],
            "icon": self.icon,
            "api": self._versions[0]["api"],
            "arch": self._versions[0]["arch"],
            "package": self.package,
            "is_game": self.category == "game",
            "screenshots": json.loads(self.screenshots),
            "versions": self._versions,
            "package_name": self.package,
            "version_name": self._versions[0]["version"],
            "min_sdk": self._versions[0]["api"],
            "category_label": category_label,
            "category_code": self.category
        }
    
class Banners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {'url':self.url, 'image':self.image}
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, primary_key=True)
    label = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text)

    def to_dict(self):
        return {
            "code": self.code,
            "label": self.label,
            "type": self.type
        }
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registeredip = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    passhash = db.Column(db.Text, nullable=False)
    regdate = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Convert the SQLAlchemy object into a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "registeredip": self.registeredip,
            "username": self.username,
            "email": self.email,
            "passhash": self.passhash
        }

class BlockedIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.Text)
    reason = db.Column(db.Text)
    blockeddate = db.Column(db.Integer)  # datetime

    def to_dict(self):
        """Convert the SQLAlchemy object into a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "ip": self.ip,
            "reason": self.reason,
            "blocked": self.blockeddate
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(25), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255))
    app_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Convert the SQLAlchemy object into a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at
        }

## TODO
# class ReviewReaction(db.Model):
#     id = db.Column(db.String(32), primary_key=True)  # userid@reviewid hashed with md5
#     user_id = db.Column(db.Integer, nullable=False)
#     review_id = db.Column(db.Integer, nullable=False)
#     reaction = db.Column(db.Integer, nullable=False)  # either -1 (dislike), 0 (nothing) or 1 (like)
#     reacted_at = db.Column(db.Integer, nullable=False)
    