from flask import Flask, render_template, redirect 
from flask import request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os 
from extension import db
from models import User



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_testing.db' 
app.secret_key = "user_name_-123"


db.init_app(app)


@app.route('/') 
def home():
    render = render_template('home.html') 
    return render 

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)