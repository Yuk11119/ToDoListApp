from app.models.sub_task import SubTask
from app.models import db

class SubTaskService:
    @staticmethod
    def get_subtasks_by_timeblock(timeblock_id):
        """获取指定时间段的所有子任务"""
        return SubTask.query.filter_by(time_block_id=timeblock_id).order_by(SubTask.order).all()
    
    @staticmethod
    def get_subtask_by_id(subtask_id):
        """根据ID获取子任务"""
        return SubTask.query.get_or_404(subtask_id)
    
    @staticmethod
    def create_subtask(subtask_data):
        """创建新的子任务"""
        new_subtask = SubTask(
            title=subtask_data['title'],
            description=subtask_data.get('description', ''),
            completed=subtask_data.get('completed', False),
            time_block_id=subtask_data['time_block_id'],
            order=subtask_data.get('order', 0)
        )
        
        db.session.add(new_subtask)
        db.session.commit()
        return new_subtask
    
    @staticmethod
    def update_subtask(subtask_id, subtask_data):
        """更新子任务"""
        subtask = SubTaskService.get_subtask_by_id(subtask_id)
        
        if 'title' in subtask_data:
            subtask.title = subtask_data['title']
        if 'description' in subtask_data:
            subtask.description = subtask_data['description']
        if 'completed' in subtask_data:
            subtask.completed = subtask_data['completed']
        if 'order' in subtask_data:
            subtask.order = subtask_data['order']
            
        db.session.commit()
        return subtask
    
    @staticmethod
    def delete_subtask(subtask_id):
        """删除子任务"""
        subtask = SubTaskService.get_subtask_by_id(subtask_id)
        db.session.delete(subtask)
        db.session.commit()
        return True
        
    @staticmethod
    def reorder_subtasks(timeblock_id, order_data):
        """重新排序子任务"""
        for item in order_data:
            subtask = SubTask.query.get(item['id'])
            if subtask and subtask.time_block_id == timeblock_id:
                subtask.order = item['order']
                
        db.session.commit()
        return True 