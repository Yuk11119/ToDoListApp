from datetime import datetime
from app import db

class CountdownTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    background_image_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'background_image_path': self.background_image_path,
            'created_at': self.created_at.isoformat()
        } 