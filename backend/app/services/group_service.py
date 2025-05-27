from app.models import db
from app.models.group import Group
from sqlalchemy.exc import IntegrityError

class GroupService:
    @staticmethod
    def get_all_groups():
        """获取所有分组"""
        return Group.query.all()
    
    @staticmethod
    def get_group_by_id(group_id):
        """根据ID获取分组"""
        return Group.query.get_or_404(group_id)
    
    @staticmethod
    def get_group_by_name(name):
        """根据名称获取分组"""
        return Group.query.filter_by(name=name).first()
    
    @staticmethod
    def create_group(group_data):
        """创建新的分组"""
        # 检查同名分组是否已存在
        existing = GroupService.get_group_by_name(group_data.get('name'))
        if existing:
            raise ValueError(f"分组 '{group_data.get('name')}' 已存在")
            
        new_group = Group(
            name=group_data.get('name'),
            description=group_data.get('description', ''),
            color=group_data.get('color', '#3498db')  # 默认蓝色
        )
        
        db.session.add(new_group)
        db.session.commit()
        return new_group
    
    @staticmethod
    def update_group(group_id, group_data):
        """更新分组信息"""
        group = GroupService.get_group_by_id(group_id)
        
        # 如果要更改名称，检查新名称是否已存在
        if 'name' in group_data and group_data['name'] != group.name:
            existing = GroupService.get_group_by_name(group_data['name'])
            if existing:
                raise ValueError(f"分组 '{group_data['name']}' 已存在")
            group.name = group_data['name']
            
        if 'description' in group_data:
            group.description = group_data['description']
            
        if 'color' in group_data:
            group.color = group_data['color']
            
        db.session.commit()
        return group
    
    @staticmethod
    def delete_group(group_id):
        """删除分组"""
        group = GroupService.get_group_by_id(group_id)
        
        # 设置相关Todo的group_id为None
        for todo in group.todos:
            todo.group_id = None
            
        db.session.delete(group)
        db.session.commit()
        return True 