from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audit.db'
db = SQLAlchemy(app)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    action = db.Column(db.String(200))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

def log_action(user_id, action):
    log = AuditLog(
        user_id=user_id,
        action=action
    )

    db.session.add(log)
    db.session.commit()

with app.app_context():
    db.create_all()

    log_action(1, "Created new product")
    log_action(2, "Deleted comment")

    logs = AuditLog.query.all()

    for l in logs:
        print(l.user_id, l.action)
