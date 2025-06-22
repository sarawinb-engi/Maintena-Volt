from extension import db 
from datetime import datetime



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_type = db.Column(db.String(100))
    task_description = db.Column(db.String(200)) 
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)