from flask import request, jsonify
from app.services.todo_service import TodoService
from app.routes import api
import json

@api.route('/todos', methods=['GET'])
def get_todos():
    """获取所有Todo任务"""
    try:
        # 检查是否指定了分组
        group = request.args.get('group')
        if group:
            todos = TodoService.get_todos_by_group(group)
        else:
            todos = TodoService.get_all_todos()
        return jsonify({'todos': [todo.to_dict() for todo in todos]}), 200
    except Exception as e:
        return jsonify({'error': f'获取任务失败: {str(e)}'}), 500

@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """获取单个Todo任务"""
    try:
        todo = TodoService.get_todo_by_id(todo_id)
        return jsonify({'todo': todo.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': f'获取任务失败: {str(e)}'}), 404

@api.route('/todos', methods=['POST'])
def create_todo():
    """创建新的Todo任务"""
    try:
        print("收到POST请求，内容:", request.data)
        data = request.get_json(force=True)
        print("解析后的JSON数据:", data)
        
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
            
        if 'title' not in data or not data['title']:
            return jsonify({'error': '标题不能为空'}), 400
            
        new_todo = TodoService.create_todo(data)
        return jsonify({'todo': new_todo.to_dict()}), 201
    except Exception as e:
        print("创建任务时出错:", str(e))
        return jsonify({'error': f'创建任务失败: {str(e)}'}), 500

@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """更新Todo任务"""
    try:
        data = request.get_json(force=True)
        todo = TodoService.update_todo(todo_id, data)
        return jsonify({'todo': todo.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': f'更新任务失败: {str(e)}'}), 500

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """删除Todo任务"""
    try:
        TodoService.delete_todo(todo_id)
        return jsonify({'message': '任务已删除'}), 200
    except Exception as e:
        return jsonify({'error': f'删除任务失败: {str(e)}'}), 500

@api.route('/groups', methods=['GET'])
def get_groups():
    """获取所有分组"""
    try:
        groups = TodoService.get_all_groups()
        return jsonify({'groups': groups}), 200
    except Exception as e:
        return jsonify({'error': f'获取分组失败: {str(e)}'}), 500 