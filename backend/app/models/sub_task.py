from datetime import datetime
from app.models import db

class SubTask(db.Model):
    __tablename__ = 'subtasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    time_block_id = db.Column(db.Integer, db.ForeignKey('time_blocks.id'), nullable=False)
    order = db.Column(db.Integer, default=0)  # 用于子任务排序
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系：多个子任务属于一个时间段
    time_block = db.relationship('TimeBlock', back_populates='subtasks')
    
    def __repr__(self):
        return f'<SubTask {self.id}: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'time_block_id': self.time_block_id,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 