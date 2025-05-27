"""
数据库重置脚本 - 当模型发生变化时使用
"""
import os
import sys
from app import create_app
from app.models import db
from app.models.todo import Todo
from app.models.group import Group

# 创建应用实例
app = create_app('development')

with app.app_context():
    # 删除所有表
    print("删除现有数据库表...")
    db.drop_all()
    
    # 创建新表
    print("创建新的数据库表...")
    db.create_all()
    
    # 添加测试分组
    print("添加测试分组...")
    test_groups = [
        Group(
            name="工作",
            description="与工作相关的任务",
            color="#FF5733"
        ),
        Group(
            name="个人",
            description="个人事务",
            color="#33A1FF"
        ),
        Group(
            name="购物",
            description="购物清单",
            color="#33FF57"
        ),
        Group(
            name="学习",
            description="学习相关任务",
            color="#F033FF"
        )
    ]
    
    for group in test_groups:
        db.session.add(group)
    
    # 提交分组以获取ID
    db.session.commit()
    
    # 获取刚刚创建的分组
    work_group = Group.query.filter_by(name="工作").first()
    shopping_group = Group.query.filter_by(name="购物").first()
    study_group = Group.query.filter_by(name="学习").first()
    
    # 添加测试任务
    print("添加测试任务...")
    test_todos = [
        Todo(
            title="完成项目报告", 
            description="需要包含项目进度和下一步计划",
            group_id=work_group.id,
            completed=False
        ),
        Todo(
            title="购买牛奶", 
            description="超市特价中",
            group_id=shopping_group.id,
            completed=True
        ),
        Todo(
            title="修复前端BUG", 
            description="用户反馈的登录问题",
            group_id=work_group.id,
            completed=False
        ),
        Todo(
            title="学习Python", 
            description="完成在线课程",
            group_id=study_group.id,
            completed=False
        )
    ]
    
    for todo in test_todos:
        db.session.add(todo)
    
    # 提交所有更改
    db.session.commit()
    
    print("数据库初始化完成!")

if __name__ == "__main__":
    print("脚本已运行完成。") 