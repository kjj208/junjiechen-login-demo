# Flask + Vue.js 登录系统

这是一个简单的登录系统，适合 Python 初学者学习。

## 功能

- 用户登录/登出
- 登录后显示 "Hello World!"
- 使用 Neon PostgreSQL 数据库存储用户信息

## 技术栈

- **前端**: 原生 HTML + JavaScript
- **后端**: Python Flask
- **数据库**: Neon PostgreSQL

## 测试账号

- 用户名: `admin`
- 密码: `admin123`

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
python app.py
```

服务器启动后访问: http://localhost:5000

## 项目结构

```
testGLM/
├── app.py              # Flask 后端服务器
├── templates/
│   ├── login.html     # 登录页面
│   └── home.html      # Hello World 页面
├── static/
│   └── js/
│       └── login.js     # JavaScript 逻辑
├── .env                # 数据库连接字符串
└── requirements.txt      # Python 依赖
```

## 数据库

- **数据库**: Neon PostgreSQL
- **表名**: users
- **字段**: id, username, password, created_at
- **测试数据**: admin/admin123
