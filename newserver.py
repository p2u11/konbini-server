from flask import render_template
import connexion
from database import db 

app = connexion.App(__name__, specification_dir="./")

flask_app = app.app
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///konbini.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(flask_app)

with flask_app.app_context():
    import models
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)