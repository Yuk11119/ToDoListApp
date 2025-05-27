from app.models.todo import Todo
from app.models import db
from app.models.group import Group
from datetime import datetime

class TodoService:
    @staticmethod
    def get_all_todos():
        """获取所有Todo任务"""
        return Todo.query.all()
    
    @staticmethod
    def get_todos_by_group(group_id):
        """根据分组获取Todo任务"""
        return Todo.query.filter_by(group_id=group_id).all()
    
    @staticmethod
    def get_todo_by_id(todo_id):
        """根据ID获取单个Todo任务"""
        return Todo.query.get_or_404(todo_id)
    
    @staticmethod
    def create_todo(todo_data):
        """创建新的Todo任务"""
        # 处理截止日期格式转换
        deadline = None
        if todo_data.get('deadline'):
            try:
                deadline = datetime.fromisoformat(todo_data['deadline'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
        
        new_todo = Todo(
            title=todo_data.get('title'),
            description=todo_data.get('description', ''),
            completed=todo_data.get('completed', False),
            group_id=todo_data.get('group_id'),  # 更新为group_id
            deadline=deadline  # 添加截止日期
        )
        db.session.add(new_todo)
        db.session.commit()
        return new_todo
    
    @staticmethod
    def update_todo(todo_id, todo_data):
        """更新指定ID的Todo任务"""
        todo = TodoService.get_todo_by_id(todo_id)
        
        if 'title' in todo_data:
            todo.title = todo_data['title']
        if 'description' in todo_data:
            todo.description = todo_data['description']
        if 'completed' in todo_data:
            todo.completed = todo_data['completed']
        if 'group_id' in todo_data:  # 更新为group_id
            todo.group_id = todo_data['group_id']
        if 'deadline' in todo_data:
            if todo_data['deadline']:
                try:
                    todo.deadline = datetime.fromisoformat(todo_data['deadline'].replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    # 如果格式无效，就保持不变
                    pass
            else:
                todo.deadline = None
        
        db.session.commit()
        return todo
    
    @staticmethod
    def delete_todo(todo_id):
        """删除指定ID的Todo任务"""
        todo = TodoService.get_todo_by_id(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return True
        
    @staticmethod
    def get_all_groups():
        """获取所有分组"""
        # 获取所有非空的分组，并去重
        groups = db.session.query(Todo.group_id).filter(Todo.group_id != None).distinct().all()
        return [group[0] for group in groups] 