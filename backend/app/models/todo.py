from datetime import datetime
from app.models import db

class Todo(db.Model):
    __tablename__ = 'todos'  # 显式指定表名
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    
    # 修改group字段为group_id外键
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    # 关联到Group模型
    group_rel = db.relationship('Group', back_populates='todos')
    
    deadline = db.Column(db.DateTime, nullable=True)  # 截止日期，可以为空
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Todo {self.id}: {self.title}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'group_id': self.group_id,
            'group': self.group_rel.name if self.group_rel else None,
            'group_color': self.group_rel.color if self.group_rel else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 