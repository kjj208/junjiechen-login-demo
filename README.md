# 简单登录系统

一个基于 Flask + Vue.js + Neon PostgreSQL 的登录系统，适合 Python 初学者学习。

## 技术栈

- **前端**: Vue.js 3 (CDN 引入，无构建工具)
- **后端**: Flask 3.0
- **数据库**: Neon PostgreSQL
- **Python 驱动**: psycopg2-binary

## 项目结构

```
testGLM/
├── app.py              # Flask 后端服务器（详细注释）
├── templates/
│   ├── login.html     # Vue.js 登录页面
│   └── home.html      # 登录后的 Hello World 页面
├── .env                # 数据库连接字符串（已配置）
└── requirements.txt      # Python 依赖列表
```

## 安装和运行

### 1. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务器

```bash
python app.py
```

服务器启动后，访问 [http://localhost:5000](http://localhost:5000)

## 测试账号

- 用户名: `admin`
- 密码: `admin123`

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/login` | POST | 登录验证 |
| `/api/check` | GET | 检查登录状态 |
| `/api/logout` | POST | 登出 |
| `/api/test-db` | GET | 测试数据库连接 |

## 学习重点

### app.py 中的 Python 概念

1. **模块导入** - `from flask import Flask`
2. **函数定义** - `def my_function():`
3. **字典操作** - `data = {'key': 'value'}`
4. **条件语句** - `if user: ... else: ...`
5. **异常处理** - `try: ... except: ...`
6. **数据库操作** - 使用 psycopg2 的游标（Cursor）

### login.html 中的 Vue.js 概念

1. **响应式数据** - `data() { return { ... } }`
2. **用户输入绑定** - `v-model="username"`
3. **事件处理** - `@submit.prevent="handleLogin"`
4. **条件渲染** - `v-if="message"`
5. **HTTP 请求** - `fetch('/api/login', ...)`

## 数据库表结构

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 注意事项

- 密码使用明文存储，仅用于学习目的
- 生产环境中应该使用密码哈希（如 bcrypt）
- Session 密钥应该使用随机生成的复杂值

## 故障排除

如果遇到连接错误：

1. 检查 Neon 项目是否正常运行
2. 验证 `.env` 文件中的连接字符串是否正确
3. 确认已安装所有依赖：`pip install -r requirements.txt`
