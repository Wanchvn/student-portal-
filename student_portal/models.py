from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    programme = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    admission_status = db.Column(db.String(20), default='Pending', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
            'gender': self.gender,
            'department': self.department,
            'programme': self.programme,
            'date_of_birth': self.date_of_birth.isoformat(),
            'image_path': self.image_path,
            'admission_status': self.admission_status,
            'created_at': self.created_at.isoformat(),
        }
