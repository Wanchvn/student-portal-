import os
import re
import uuid
from datetime import datetime

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from config import ALLOWED_EXTENSIONS
from models import Student, db

web_bp = Blueprint('web', __name__)

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_PATTERN = re.compile(r'^\+?[\d\s\-()]{7,20}$')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(file):
    if not file or file.filename == '':
        return None, 'Profile image is required.'

    if not allowed_file(file.filename):
        return None, 'Only JPG, JPEG, and PNG images are allowed.'

    original = secure_filename(file.filename)
    name, ext = os.path.splitext(original)
    unique_name = f'{name}_{uuid.uuid4().hex[:8]}{ext}'
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, unique_name)

    try:
        file.save(filepath)
    except OSError:
        return None, 'Failed to save uploaded image. Please try again.'

    return unique_name, None


def validate_registration_form(form, has_image):
    errors = {}

    full_name = form.get('full_name', '').strip()
    if not full_name:
        errors['full_name'] = 'Full name is required.'

    address = form.get('address', '').strip()
    if not address:
        errors['address'] = 'Address is required.'

    email = form.get('email', '').strip()
    if not email:
        errors['email'] = 'Email is required.'
    elif not EMAIL_PATTERN.match(email):
        errors['email'] = 'Please enter a valid email address.'

    phone = form.get('phone', '').strip()
    if not phone:
        errors['phone'] = 'Phone number is required.'
    elif not PHONE_PATTERN.match(phone):
        errors['phone'] = 'Please enter a valid phone number.'

    date_of_birth = form.get('date_of_birth', '').strip()
    if not date_of_birth:
        errors['date_of_birth'] = 'Date of birth is required.'
    else:
        try:
            datetime.strptime(date_of_birth, '%Y-%m-%d')
        except ValueError:
            errors['date_of_birth'] = 'Please enter a valid date.'

    gender = form.get('gender', '').strip()
    if gender not in ('Male', 'Female'):
        errors['gender'] = 'Please select a gender.'

    department = form.get('department', '').strip()
    if not department:
        errors['department'] = 'Please select a department.'

    programme = form.get('programme', '').strip()
    if not programme:
        errors['programme'] = 'Please select a programme.'

    if not has_image:
        errors['image'] = 'Profile image is required.'

    return errors


@web_bp.route('/')
def index():
    return render_template('index.html')


@web_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    form = request.form
    image_file = request.files.get('image')
    has_image = image_file and image_file.filename != ''
    errors = validate_registration_form(form, has_image)

    if errors:
        for message in errors.values():
            flash(message, 'danger')
        return render_template('register.html', form_data=form, errors=errors), 400

    image_path, upload_error = save_uploaded_image(image_file)
    if upload_error:
        flash(upload_error, 'danger')
        return render_template('register.html', form_data=form, errors={'image': upload_error}), 400

    try:
        student = Student(
            full_name=form.get('full_name').strip(),
            address=form.get('address').strip(),
            email=form.get('email').strip(),
            phone=form.get('phone').strip(),
            gender=form.get('gender'),
            department=form.get('department'),
            programme=form.get('programme'),
            date_of_birth=datetime.strptime(form.get('date_of_birth'), '%Y-%m-%d').date(),
            image_path=image_path,
            admission_status=form.get('admission_status', 'Pending') or 'Pending',
        )
        db.session.add(student)
        db.session.commit()
    except Exception:
        db.session.rollback()
        if image_path:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
            if os.path.exists(filepath):
                os.remove(filepath)
        flash('Registration failed. Email may already be registered.', 'danger')
        return render_template('register.html', form_data=form), 500

    flash('Registration successful!', 'success')
    return redirect(url_for('web.students'))


@web_bp.route('/students')
def students():
    all_students = Student.query.order_by(Student.created_at.desc()).all()
    return render_template('students.html', students=all_students)


@web_bp.route('/student/<int:id>')
def student_details(id):
    student = Student.query.get_or_404(id)
    return render_template('student_details.html', student=student)


@web_bp.route('/about')
def about():
    return render_template('about.html')
