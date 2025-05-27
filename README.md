# Todo 应用

一个使用 Vue.js 和 Flask 构建的前后端分离的 Todo 应用。

## 项目结构

```
ToDoListApp-2/
├── backend/            # Flask 后端
│   ├── app/            # 应用代码
│   │   ├── models/     # 数据模型
│   │   ├── routes/     # API路由
│   │   ├── services/   # 业务逻辑
│   │   └── utils/      # 工具函数
│   ├── instance/       # 实例配置
│   ├── venv/           # Python虚拟环境
│   ├── .env            # 环境变量
│   ├── config.py       # 配置文件
│   ├── requirements.txt# 依赖列表
│   └── run.py          # 应用入口
└── frontend/           # Vue.js 前端
    ├── src/            # 源代码
    │   ├── api/        # API调用
    │   ├── assets/     # 静态资源
    │   ├── components/ # 组件
    │   ├── router/     # 路由配置
    │   ├── views/      # 视图
    │   ├── App.vue     # 根组件
    │   └── main.js     # 入口文件
    ├── public/         # 公共文件
    ├── index.html      # HTML模板
    ├── package.json    # 依赖管理
    └── vite.config.js  # Vite配置
```

## 功能特性

- 创建、查看、编辑和删除任务
- 标记任务为已完成/未完成
- 查看任务详情

## 技术栈

### 前端
- Vue.js 3
- Vue Router
- Axios
- Vite

### 后端
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- SQLite数据库

## 模块化分层设计

为了保持代码清晰和可维护，同时避免过度设计，本项目采用轻量级分层架构：

### 后端分层架构

#### 1. 模型层 (Models)
- 职责：定义数据结构和数据库交互
- 位置：`backend/app/models/`
- 示例：

```python
# app/models/todo.py
from app.models import db

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # 其他字段...
```

#### 2. 服务层 (Services)
- 职责：处理业务逻辑，封装数据库操作
- 位置：`backend/app/services/`
- 示例：

```python
# app/services/todo_service.py
from app.models.todo import Todo
from app.models import db

class TodoService:
    @staticmethod
    def get_all_todos():
        return Todo.query.all()
        
    @staticmethod
    def create_todo(todo_data):
        new_todo = Todo(**todo_data)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo
```

#### 3. 路由层 (Routes)
- 职责：定义API端点，调用服务层处理请求
- 位置：`backend/app/routes/`
- 示例：

```python
# app/routes/todo_routes.py
from flask import request, jsonify
from app.services.todo_service import TodoService

@api.route('/todos', methods=['GET'])
def get_todos():
    todos = TodoService.get_all_todos()
    return jsonify({'todos': [todo.to_dict() for todo in todos]})
```

### 前端分层架构

#### 1. API层
- 职责：封装与后端通信的逻辑
- 位置：`frontend/src/api/`
- 示例：

```javascript
// src/api/todo-api.js
import axios from 'axios';

const api = axios.create({
  baseURL: '/api'
});

export const TodoAPI = {
  getAllTodos() {
    return api.get('/todos');
  },
  
  createTodo(todo) {
    return api.post('/todos', todo);
  }
};
```

#### 2. 组件层
- 职责：实现可复用的UI组件
- 位置：`frontend/src/components/`
- 示例：接收props并发出事件的独立组件

#### 3. 视图层
- 职责：整合组件和API调用，实现页面功能
- 位置：`frontend/src/views/`
- 示例：包含页面布局和数据管理逻辑

## 分层设计的优势

1. **关注点分离**：每层只专注于自己的职责
2. **代码复用**：通用逻辑可以在不同组件间共享
3. **易于维护**：修改某一层时不影响其他层
4. **测试友好**：各层可以独立测试

## 安装与运行

### 后端

1. 进入后端目录
```bash
cd backend
```

2. 激活虚拟环境
```bash
source venv/bin/activate  # 在Linux/Mac上
# 或
venv\Scripts\activate     # 在Windows上
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
python run.py
```

后端服务将在 http://localhost:5000 上运行。

### 前端

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 运行开发服务器
```bash
npm run dev
```

前端应用将在 http://localhost:3000 上运行。

## API文档

### 获取所有任务
- GET /api/todos

### 获取单个任务
- GET /api/todos/:id

### 创建任务
- POST /api/todos
- Body: { "title": "任务标题", "description": "任务描述", "completed": false }

### 更新任务
- PUT /api/todos/:id
- Body: { "title": "更新的标题", "description": "更新的描述", "completed": true }

### 删除任务
- DELETE /api/todos/:id 