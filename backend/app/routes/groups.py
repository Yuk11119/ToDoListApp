from flask import Blueprint, jsonify, request
from app.services.group_service import GroupService

groups_bp = Blueprint('groups', __name__, url_prefix='/api/groups')

@groups_bp.route('', methods=['GET'])
def get_all_groups():
    """获取所有分组"""
    groups = GroupService.get_all_groups()
    return jsonify({
        'success': True,
        'data': [group.to_dict() for group in groups]
    }), 200

@groups_bp.route('/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """获取单个分组"""
    try:
        group = GroupService.get_group_by_id(group_id)
        return jsonify({
            'success': True,
            'data': group.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@groups_bp.route('', methods=['POST'])
def create_group():
    """创建分组"""
    data = request.json
    
    if not data or not data.get('name'):
        return jsonify({
            'success': False,
            'error': '分组名称不能为空'
        }), 400
    
    try:
        new_group = GroupService.create_group(data)
        return jsonify({
            'success': True,
            'data': new_group.to_dict(),
            'message': '分组创建成功'
        }), 201
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'创建分组失败: {str(e)}'
        }), 500

@groups_bp.route('/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    """更新分组"""
    data = request.json
    
    if not data:
        return jsonify({
            'success': False,
            'error': '数据不能为空'
        }), 400
    
    try:
        updated_group = GroupService.update_group(group_id, data)
        return jsonify({
            'success': True,
            'data': updated_group.to_dict(),
            'message': '分组更新成功'
        }), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'更新分组失败: {str(e)}'
        }), 500

@groups_bp.route('/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """删除分组"""
    try:
        GroupService.delete_group(group_id)
        return jsonify({
            'success': True,
            'message': '分组已删除'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'删除分组失败: {str(e)}'
        }), 500 