from database import db
from models import Review
from sqlalchemy import or_, select, and_
import traceback, auth, time, app, datetime

def get_reviews(app_id):
    reviews = db.session.scalars(select(Review).where(Review.app_id == app_id).order_by(Review.created_at.desc())).all()
    return [dict(review.to_dict(), created_at=datetime.datetime.utcfromtimestamp(review.created_at).strftime('%Y-%m-%d %H:%M:%S'), likes=0, dislikes=0, comment_count=0) for review in reviews]

# TODO
def get_review(review_id):
    ...
#    reviews = db.session.scalars(select(Review).where(Review.app_id == app_id).order_by(Review.created_at.desc())).all()
#     return [dict(review.to_dict(), likes=0, dislikes=0, comment_count=0) for review in reviews]

# FIXME: VERY INSECURE!! TODO: make a token system
def add_review(app_id: int, body: dict):
    user_id, comment, rating = body.get('user_id'), body.get('comment'), body.get('rating')

    if not user_id or not rating:
        return {'error':'user_id and rating fields are required'}, 400
    
    user = auth.user_by_id(user_id)

    if not user:
        return {'error':f'User {user_id} not found'}, 400
    
    if app.api_app(app_id)[1] == 404:
        return {'error':f'App {app_id} not found'}, 400

    if len(comment) > 255:
        return {'error':'comment too big'}, 400

    review = Review(
        user_id = user_id,
        username = user['username'],
        rating = rating,
        comment = comment,
        app_id = app_id,
        created_at = time.time()
    )

    try:
        db.session.add(review)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return {"error": "Internal server error"}, 500
    return {"success": True, "message": "Review added successfully"}, 201

# TODO: make a token system and implement this
def set_review_reaction(review_id:int, body:dict):
    return {'error':'Not implemented'}, 500
#     user_id, value = body.get('user_id'), body.get('value')

#     if not user_id:
#         return {"error": "User ID is required"}, 401
#     if value not in (-1, 0, 1):
#         return {"error": "Invalid value"}, 400
    
#     user = auth.user_by_id
    
#     review = db.session.scalars(select(Review).where(Review.id == review_id).limit(1)).all()

#     if len(review) <= 0:
#         return {"error": "Review not found"}, 404
    
#     existing = ReviewReaction.query.filter_by(review_id=review_id, user_id=user_id).first()
#     if existing:
#         existing.value = value
#     else:
#         db.session.add(ReviewReaction(review_id=review_id, user_id=user_id, value=value))
#     db.session.add(ReactionIP(review_id=review_id, ip=ip))
#     db.session.commit()
#     likes = db.
#     likes = ReviewReaction.query.filter_by(review_id=review_id, value=1).count()
#     dislikes = ReviewReaction.query.filter_by(review_id=review_id, value=-1).count()
#     return {"success": True, "likes": likes, "dislikes": dislikes, "user_reaction": value}
#     return params