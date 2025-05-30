import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models.countdown_task import CountdownTask

countdown_tasks = Blueprint('countdown_tasks', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@countdown_tasks.route('/api/countdown-tasks', methods=['GET'])
def get_all_countdown_tasks():
    countdown_tasks = CountdownTask.query.order_by(CountdownTask.deadline).all()
    return jsonify([task.to_dict() for task in countdown_tasks])

@countdown_tasks.route('/api/countdown-tasks/<int:id>', methods=['GET'])
def get_countdown_task(id):
    task = CountdownTask.query.get_or_404(id)
    return jsonify(task.to_dict())

@countdown_tasks.route('/api/countdown-tasks', methods=['POST'])
def create_countdown_task():
    data = request.form.to_dict()
    
    # 处理日期
    if 'deadline' in data:
        try:
            data['deadline'] = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': '日期格式无效'}), 400
    
    # 处理图片上传
    background_image = request.files.get('background_image')
    background_image_path = None
    
    if background_image and background_image.filename != '' and allowed_file(background_image.filename):
        # 确保上传目录存在
        upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'countdown_backgrounds')
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        filename = secure_filename(background_image.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        background_image.save(file_path)
        
        # 保存相对路径
        background_image_path = f"uploads/countdown_backgrounds/{unique_filename}"
    
    # 创建任务
    new_task = CountdownTask(
        name=data.get('name'),
        deadline=data.get('deadline'),
        background_image_path=background_image_path
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify(new_task.to_dict()), 201

@countdown_tasks.route('/api/countdown-tasks/<int:id>', methods=['PUT'])
def update_countdown_task(id):
    task = CountdownTask.query.get_or_404(id)
    data = request.form.to_dict()
    
    # 处理日期
    if 'deadline' in data:
        try:
            data['deadline'] = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': '日期格式无效'}), 400
    
    # 处理图片上传
    background_image = request.files.get('background_image')
    
    if background_image and background_image.filename != '' and allowed_file(background_image.filename):
        # 删除旧图片
        if task.background_image_path:
            old_image_path = os.path.join(current_app.root_path, '..', task.background_image_path)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        
        # 确保上传目录存在
        upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'countdown_backgrounds')
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        filename = secure_filename(background_image.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        background_image.save(file_path)
        
        # 更新路径
        task.background_image_path = f"uploads/countdown_backgrounds/{unique_filename}"
    
    # 更新其他字段
    if 'name' in data:
        task.name = data['name']
    if 'deadline' in data:
        task.deadline = data['deadline']
    
    db.session.commit()
    
    return jsonify(task.to_dict())

@countdown_tasks.route('/api/countdown-tasks/<int:id>', methods=['DELETE'])
def delete_countdown_task(id):
    task = CountdownTask.query.get_or_404(id)
    
    # 删除关联的背景图片
    if task.background_image_path:
        image_path = os.path.join(current_app.root_path, '..', task.background_image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': '倒计时任务已删除'}) 