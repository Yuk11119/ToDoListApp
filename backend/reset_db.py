"""
数据库重置脚本 - 当模型发生变化时使用
"""
import os
import sys
from datetime import date
from app import create_app
from app.models import db
from app.models.todo import Todo
from app.models.group import Group
from app.models.time_block import TimeBlock
from app.models.sub_task import SubTask

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
    
    # 添加测试时间段任务
    print("添加测试时间段任务...")
    
    # 获取当前日期
    today = date.today()
    
    # 创建测试时间段
    test_timeblocks = [
        TimeBlock(
            start_date=date(today.year, today.month, today.day),
            end_date=date(today.year, today.month, today.day + 2)
        ),
        TimeBlock(
            start_date=date(today.year, today.month, today.day + 5),
            end_date=date(today.year, today.month, today.day + 10)
        ),
        TimeBlock(
            start_date=date(today.year, today.month + 1, 1),
            end_date=date(today.year, today.month + 1, 5)
        )
    ]
    
    for timeblock in test_timeblocks:
        db.session.add(timeblock)
        
    # 提交时间段以获取ID
    db.session.commit()
    
    # 获取刚刚创建的时间段
    first_block = test_timeblocks[0]
    second_block = test_timeblocks[1]
    third_block = test_timeblocks[2]
    
    # 为时间段添加子任务
    test_subtasks = [
        # 第一个时间段的子任务
        SubTask(title="检查邮件", time_block_id=first_block.id, order=0),
        SubTask(title="回复重要邮件", description="优先处理客户邮件", time_block_id=first_block.id, order=1),
        SubTask(title="安排每日会议", time_block_id=first_block.id, order=2),
        SubTask(title="准备项目报告", time_block_id=first_block.id, order=3),
        
        # 第二个时间段的子任务
        SubTask(title="阅读技术文章", time_block_id=second_block.id, order=0),
        SubTask(title="完成在线课程", description="完成Vue.js高级课程第3章", time_block_id=second_block.id, order=1),
        SubTask(title="实践新技术", time_block_id=second_block.id, order=2),
        
        # 第三个时间段的子任务
        SubTask(title="列出明日待办事项", time_block_id=third_block.id, order=0),
        SubTask(title="规划项目时间表", time_block_id=third_block.id, order=1),
        SubTask(title="设置提醒", time_block_id=third_block.id, order=2)
    ]
    
    for subtask in test_subtasks:
        db.session.add(subtask)
    
    # 提交所有更改
    db.session.commit()
    
    print("数据库初始化完成!")

if __name__ == "__main__":
    print("脚本已运行完成。") 