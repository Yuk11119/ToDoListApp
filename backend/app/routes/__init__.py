from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')
 
from app.routes import todo_routes 