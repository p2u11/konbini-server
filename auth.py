from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from database import db
from models import User, BlockedIP
from sqlalchemy import or_, select, and_, cast, Integer, func
from time import time
import re, misc, traceback

ph = PasswordHasher()

def user_by_id(user_id: int) -> dict | None:
    app = db.session.scalars(select(User).where(User.id == user_id).limit(1)).all()
    return app[0].to_dict() if app else None

def user_exists(username: str) -> list:
    app = db.session.scalars(select(User).where(User.username == username).limit(1)).all()
    return app

def is_ip_blocked(ip: str) -> bool:
    ban = db.session.scalars(select(BlockedIP).where(BlockedIP.ip == ip).limit(1)).all()
    return len(ban) > 0

def check_registration_rate_limit(ip: str, limit_per_day: int = 3) -> bool:
    one_day_ago = time() - 86400
    
    stmt = (
        select(func.count(User.id))
        .where(User.registeredip == ip)
        .where(User.regdate >= one_day_ago)
    )
    
    registered_count = db.session.scalar(stmt) or 0
    
    return registered_count < limit_per_day

# TODO: make a token system
def login(body: dict):
    username, password = body.get('username'), body.get('password')
    user = user_exists(username)

    if not user:
        try: ph.verify('$argon2id$v=19$m=65536,t=3,p=4$Up6SP61+bKlJrRfgAvm6nQ$1Mi7OxznzG+qyqsA9qvNcUiZjrnOTTqxMCC4fHzk/BQ', '456')
        except VerifyMismatchError: ...
        return {'error':'Invalid credentials'}, 401
    
    user = user[0].to_dict()

    try: ph.verify(user['passhash'], password)
    except VerifyMismatchError:
        return {'error':'Invalid credentials'}, 401
    
    return {"success": True, "user_id": user['id'], "username": user['username']}, 200

def register(body: dict):
    username, email, password = body.get('username'), body.get('email'), body.get('password')
    ip = misc.get_ip()

    if is_ip_blocked(ip):
        return {"error": "IP blocked"}, 429
    if not check_registration_rate_limit(ip):
        return {"error": "Too many registrations from this IP today"}, 429
    
    if not username or not email or not password:
        return {"error": "All fields are required"}, 400
    
    if len(username) < 3 or len(username) > 32:
        return {"error": "Username must be between 3 and 32 chars"}, 400
    if not re.match(r'^[a-zA-Z0-9_\-]+$', username):
        return {"error": "Username contains invalid characters"}, 400
    
    if len(password) < 6:
        return {"error": "Password must be at least 6 characters"}, 400
    
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return {"error": "Invalid email"}, 400
    
    if user_exists(username):
        return {"error": "Username already exists"}, 400
    
    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 400
    
    passhash = ph.hash(password)

    user = User(
        registeredip=ip,
        username=username,
        email=email,
        passhash=passhash,
        regdate=time()
    )

    try:
        db.session.add(user)
        db.session.commit()
        return {
            "message": "User created successfully",
            "user_id": user.id,
            "username": user.username
        }, 201
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return {"error": "Internal server error"}, 500
