from app.models.time_block import TimeBlock
from app.models import db
from datetime import datetime, date

class TimeBlockService:
    @staticmethod
    def get_all_timeblocks():
        """获取所有时间段任务"""
        return TimeBlock.query.all()
    
    @staticmethod
    def get_timeblock_by_id(timeblock_id):
        """根据ID获取时间段任务"""
        return TimeBlock.query.get_or_404(timeblock_id)
    
    @staticmethod
    def create_timeblock(timeblock_data):
        """创建新的时间段任务"""
        # 从ISO日期字符串转换为日期对象
        if 'start_date' in timeblock_data and isinstance(timeblock_data['start_date'], str):
            start_date = datetime.fromisoformat(timeblock_data['start_date'].replace('Z', '+00:00')).date()
        else:
            start_date = timeblock_data['start_date']
            
        if 'end_date' in timeblock_data and isinstance(timeblock_data['end_date'], str):
            end_date = datetime.fromisoformat(timeblock_data['end_date'].replace('Z', '+00:00')).date()
        else:
            end_date = timeblock_data['end_date']
        
        new_timeblock = TimeBlock(
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(new_timeblock)
        db.session.commit()
        return new_timeblock
    
    @staticmethod
    def update_timeblock(timeblock_id, timeblock_data):
        """更新时间段任务"""
        timeblock = TimeBlockService.get_timeblock_by_id(timeblock_id)
        
        if 'start_date' in timeblock_data:
            if isinstance(timeblock_data['start_date'], str):
                timeblock.start_date = datetime.fromisoformat(timeblock_data['start_date'].replace('Z', '+00:00')).date()
            else:
                timeblock.start_date = timeblock_data['start_date']
                
        if 'end_date' in timeblock_data:
            if isinstance(timeblock_data['end_date'], str):
                timeblock.end_date = datetime.fromisoformat(timeblock_data['end_date'].replace('Z', '+00:00')).date()
            else:
                timeblock.end_date = timeblock_data['end_date']
            
        db.session.commit()
        return timeblock
    
    @staticmethod
    def delete_timeblock(timeblock_id):
        """删除时间段任务"""
        timeblock = TimeBlockService.get_timeblock_by_id(timeblock_id)
        db.session.delete(timeblock)
        db.session.commit()
        return True 