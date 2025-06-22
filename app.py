from flask import Flask, render_template, redirect 
from flask import request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os 
from extension import db
from models import User, Task



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_testing.db' 
app.secret_key = "user_name_-123"


db.init_app(app)


@app.route('/') 
def index():
    homepage = render_template('index.html') 
    return homepage 


@app.route('/home', methods=['POST', 'GET'])
def home():
    equipment_type = request.form.get('equipment_type')
    task_description = request.form.get('task_description') 
    status = request.form.get('status')
    
    new_task = Task(
        equipment_type = equipment_type, 
        task_description = task_description, 
        status = status
    )   
    db.session.add(new_task) 
    db.session.commit() 
    
    flash('Addition Worked Succuss!', 'success')
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email = request.form.get('email') 
        password = request.form.get('password')
        
        if email and password:
            user = User.query.filter_by(email=email).first()
            session['username'] = user.username
            flash('Login successful!', 'success') 
            return redirect('/dashboard')
        else:
            flash('Invalid email or password', 'danger')
    else:
        flash('Please enter both email and password', 'warning')
        
    login_page = render_template('login.html')

    return login_page


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username') 
        email = request.form.get('email') 
        password = request.form.get('password')
        
        if username and email and password:
            existing_user = User.query.filter_by(email=email).first()
            
            if existing_user:
                flash('Email already exits', 'danger')
                
                return redirect('/register')            
            
            new_usr = User(username=username,
                           email=email,
                           password=generate_password_hash(password))
            db.session.add(new_usr) 
            db.session.commit() 
            flash('Registration successful!', 'success') 
            
            return redirect('/login') 

        else:
            flash('Please fill in all fields', 'warning') 
            return redirect('/register') 
        
    regis = render_template('register.html')

    return regis


@app.route('/dashboard')
def dashboard(): 
    total_task = Task.query.count() 
    completed_tasks = Task.query.filter_by(status='Completed').count() 
    pending_tasks = Task.query.filter_by(status='Pendinf').count() 
    
    
    
    return render_template('dashboard.html', 
                           total_task=total_task,
                           completed_tasks=completed_tasks,
                           pending_tasks=pending_tasks)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
    
    



if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)