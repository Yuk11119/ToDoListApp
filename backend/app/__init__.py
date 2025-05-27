from flask import Flask, jsonify
from flask_cors import CORS
from app.models import db
from config import config

def create_app(config_name='default'):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(flask_app)
    
    # 启用CORS
    CORS(flask_app)
    
    # 注册蓝图
    from app.routes.todos import todos_bp
    from app.routes.groups import groups_bp
    
    flask_app.register_blueprint(todos_bp)
    flask_app.register_blueprint(groups_bp)
    
    @flask_app.route('/')
    def index():
        return jsonify({'message': 'Welcome to the Todo API!'})
    
    return flask_app 