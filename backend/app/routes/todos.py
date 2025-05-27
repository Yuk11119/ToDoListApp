from flask import Blueprint, jsonify, request
from app.services.todo_service import TodoService
from app.services.group_service import GroupService

todos_bp = Blueprint('todos', __name__, url_prefix='/api/todos')

@todos_bp.route('', methods=['GET'])
def get_todos():
    group_id = request.args.get('group_id')
    
    if group_id:
        todos = TodoService.get_todos_by_group(int(group_id))
    else:
        todos = TodoService.get_all_todos()
    
    return jsonify({
        'success': True,
        'data': [todo.to_dict() for todo in todos]
    }), 200

@todos_bp.route('/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    try:
        todo = TodoService.get_todo_by_id(todo_id)
        return jsonify({
            'success': True,
            'data': todo.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@todos_bp.route('', methods=['POST'])
def create_todo():
    data = request.json
    
    if not data or 'title' not in data:
        return jsonify({
            'success': False,
            'error': '任务标题不能为空'
        }), 400
    
    try:
        new_todo = TodoService.create_todo(data)
        return jsonify({
            'success': True,
            'data': new_todo.to_dict(),
            'message': '任务创建成功'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'创建任务失败: {str(e)}'
        }), 500

@todos_bp.route('/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    
    if not data:
        return jsonify({
            'success': False,
            'error': '数据不能为空'
        }), 400
    
    try:
        updated_todo = TodoService.update_todo(todo_id, data)
        return jsonify({
            'success': True,
            'data': updated_todo.to_dict(),
            'message': '任务更新成功'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'更新任务失败: {str(e)}'
        }), 500

@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        TodoService.delete_todo(todo_id)
        return jsonify({
            'success': True,
            'message': '任务已删除'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'删除任务失败: {str(e)}'
        }), 500 