from datetime import datetime
from app.models import db

class TimeBlock(db.Model):
    __tablename__ = 'time_blocks'
    
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系：一个时间段可以包含多个子任务
    subtasks = db.relationship('SubTask', back_populates='time_block', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<TimeBlock {self.id}: {self.start_date} to {self.end_date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'subtasks': [subtask.to_dict() for subtask in self.subtasks],
            'progress': self.calculate_progress()
        }
    
    def calculate_progress(self):
        if not self.subtasks:
            return 0
        completed = sum(1 for task in self.subtasks if task.completed)
        return int((completed / len(self.subtasks)) * 100) 