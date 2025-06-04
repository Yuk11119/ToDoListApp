from flask import Blueprint, jsonify, request
from app.services.time_block_service import TimeBlockService
from app.services.sub_task_service import SubTaskService

# 创建蓝图
timeblocks_bp = Blueprint('timeblocks', __name__, url_prefix='/api/timeblocks')

@timeblocks_bp.route('', methods=['GET'])
def get_timeblocks():
    """获取所有时间段任务"""
    timeblocks = TimeBlockService.get_all_timeblocks()
    return jsonify({
        'success': True,
        'data': [timeblock.to_dict() for timeblock in timeblocks]
    }), 200

@timeblocks_bp.route('/<int:timeblock_id>', methods=['GET'])
def get_timeblock(timeblock_id):
    """获取单个时间段任务"""
    try:
        timeblock = TimeBlockService.get_timeblock_by_id(timeblock_id)
        return jsonify({
            'success': True,
            'data': timeblock.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@timeblocks_bp.route('', methods=['POST'])
def create_timeblock():
    """创建时间段任务"""
    data = request.json
    
    if not data or 'start_date' not in data or 'end_date' not in data:
        return jsonify({
            'success': False,
            'error': '时间范围不能为空'
        }), 400
    
    try:
        new_timeblock = TimeBlockService.create_timeblock(data)
        return jsonify({
            'success': True,
            'data': new_timeblock.to_dict(),
            'message': '时间段任务创建成功'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'创建时间段任务失败: {str(e)}'
        }), 500

@timeblocks_bp.route('/<int:timeblock_id>', methods=['PUT'])
def update_timeblock(timeblock_id):
    """更新时间段任务"""
    data = request.json
    
    try:
        updated_timeblock = TimeBlockService.update_timeblock(timeblock_id, data)
        return jsonify({
            'success': True,
            'data': updated_timeblock.to_dict(),
            'message': '时间段任务更新成功'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'更新时间段任务失败: {str(e)}'
        }), 500

@timeblocks_bp.route('/<int:timeblock_id>', methods=['DELETE'])
def delete_timeblock(timeblock_id):
    """删除时间段任务"""
    try:
        TimeBlockService.delete_timeblock(timeblock_id)
        return jsonify({
            'success': True,
            'message': '时间段任务已删除'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'删除时间段任务失败: {str(e)}'
        }), 500

# 子任务相关路由
@timeblocks_bp.route('/<int:timeblock_id>/subtasks', methods=['GET'])
def get_subtasks(timeblock_id):
    """获取时间段下的所有子任务"""
    try:
        subtasks = SubTaskService.get_subtasks_by_timeblock(timeblock_id)
        return jsonify({
            'success': True,
            'data': [subtask.to_dict() for subtask in subtasks]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@timeblocks_bp.route('/<int:timeblock_id>/subtasks', methods=['POST'])
def create_subtask(timeblock_id):
    """创建子任务"""
    data = request.json
    
    if not data or 'title' not in data:
        return jsonify({
            'success': False,
            'error': '子任务标题不能为空'
        }), 400
    
    # 确保子任务与正确的时间段关联
    data['time_block_id'] = timeblock_id
    
    try:
        new_subtask = SubTaskService.create_subtask(data)
        return jsonify({
            'success': True,
            'data': new_subtask.to_dict(),
            'message': '子任务创建成功'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'创建子任务失败: {str(e)}'
        }), 500
        
@timeblocks_bp.route('/<int:timeblock_id>/subtasks/<int:subtask_id>', methods=['PUT'])
def update_subtask(timeblock_id, subtask_id):
    """更新子任务"""
    data = request.json
    
    try:
        subtask = SubTaskService.get_subtask_by_id(subtask_id)
        # 检查子任务是否属于指定的时间段
        if subtask.time_block_id != timeblock_id:
            return jsonify({
                'success': False,
                'error': '子任务不属于指定的时间段'
            }), 400
            
        updated_subtask = SubTaskService.update_subtask(subtask_id, data)
        return jsonify({
            'success': True,
            'data': updated_subtask.to_dict(),
            'message': '子任务更新成功'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'更新子任务失败: {str(e)}'
        }), 500

@timeblocks_bp.route('/<int:timeblock_id>/subtasks/<int:subtask_id>', methods=['DELETE'])
def delete_subtask(timeblock_id, subtask_id):
    """删除子任务"""
    try:
        subtask = SubTaskService.get_subtask_by_id(subtask_id)
        # 检查子任务是否属于指定的时间段
        if subtask.time_block_id != timeblock_id:
            return jsonify({
                'success': False,
                'error': '子任务不属于指定的时间段'
            }), 400
            
        SubTaskService.delete_subtask(subtask_id)
        return jsonify({
            'success': True,
            'message': '子任务已删除'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'删除子任务失败: {str(e)}'
        }), 500

@timeblocks_bp.route('/<int:timeblock_id>/subtasks/reorder', methods=['POST'])
def reorder_subtasks(timeblock_id):
    """重新排序子任务"""
    data = request.json
    
    if not data or not isinstance(data, list):
        return jsonify({
            'success': False,
            'error': '请求数据格式错误'
        }), 400
        
    try:
        SubTaskService.reorder_subtasks(timeblock_id, data)
        return jsonify({
            'success': True,
            'message': '子任务排序成功'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'子任务排序失败: {str(e)}'
        }), 500 