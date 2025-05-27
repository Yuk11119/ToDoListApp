from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(flask_app):
    db.init_app(flask_app)
    
    # 导入所有模型，确保它们在创建表之前被注册
    from app.models import todo
    
    with flask_app.app_context():
        db.create_all() 