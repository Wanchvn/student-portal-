from flask import Blueprint, jsonify, request

from models import Student, db

api_bp = Blueprint('api', __name__, url_prefix='/api')

DEPARTMENTS = [
    {'id': 1, 'name': 'Computer Science'},
    {'id': 2, 'name': 'Information Technology'},
    {'id': 3, 'name': 'Cyber Security'},
    {'id': 4, 'name': 'Networking'},
]

PROGRAMMES = [
    {'id': 1, 'name': 'Bachelor of Science'},
    {'id': 2, 'name': 'Bachelor of Technology'},
    {'id': 3, 'name': 'Diploma'},
    {'id': 4, 'name': 'Master of Science'},
]

VALID_STATUSES = ('Pending', 'Admitted', 'Rejected')


@api_bp.route('/departments')
def get_departments():
    return jsonify(DEPARTMENTS)


@api_bp.route('/programmes')
def get_programmes():
    return jsonify(PROGRAMMES)


@api_bp.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'success': False, 'message': 'Student not found.'}), 404

    data = request.get_json(silent=True)
    if not data or 'status' not in data:
        return jsonify({'success': False, 'message': 'Status is required.'}), 400

    status = data['status'].strip()
    if status not in VALID_STATUSES:
        return jsonify({'success': False, 'message': 'Invalid admission status.'}), 400

    student.admission_status = status
    db.session.commit()

    return jsonify({'success': True})
