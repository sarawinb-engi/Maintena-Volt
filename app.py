from flask import Flask, render_template, redirect, url_for
from flask import request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os 
from extension import db
from models import User, RepairReport
from werkzeug.utils import secure_filename



app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_testing.db' 
app.secret_key = "user_name_-123"

db.init_app(app)


@app.route('/') 
def index():
    homepage = render_template('index.html') 
    return homepage 


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # ดึงค่าจากฟอร์ม
        issue_type = request.form.get('issue_type')
        issue_type_other = request.form.get('issue_type_other')
        subject = request.form.get('subject')
        description = request.form.get('description')
        location = request.form.get('location')
        reporter = request.form.get('reporter')
        contact = request.form.get('contact')

        # แก้ไขประเภทปัญหาหากเลือก "อื่นๆ"
        if issue_type == 'อื่นๆ' and issue_type_other:
            issue_type = issue_type_other

        # จัดการรูปภาพ (สูงสุด 3 รูป)
        uploaded_files = request.files.getlist('photos')
        photo_filenames = []

        for file in uploaded_files[:3]:  # จำกัดไม่เกิน 3 รูป
            if file and file.filename:
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                photo_filenames.append(filename)

        # บันทึกลงฐานข้อมูล
        new_report = RepairReport(
            issue_type=issue_type,
            subject=subject,
            description=description,
            location=location,
            reporter=reporter,
            contact=contact,
            photo1=photo_filenames[0] if len(photo_filenames) > 0 else None,
            photo2=photo_filenames[1] if len(photo_filenames) > 1 else None,
            photo3=photo_filenames[2] if len(photo_filenames) > 2 else None
        )

        db.session.add(new_report)
        db.session.commit()
        flash('ส่งเรื่องแจ้งซ่อมเรียบร้อยแล้ว ✅', 'success')
        return redirect(url_for('report'))

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

    
    
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
    
    



if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)