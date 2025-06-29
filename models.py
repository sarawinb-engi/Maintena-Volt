from extension import db 
from datetime import datetime



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    


class RepairReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_type = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    reporter = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    photo1 = db.Column(db.String(200))
    photo2 = db.Column(db.String(200))
    photo3 = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())