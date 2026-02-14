#!/usr/bin/env python3
# ============================================================
# app.py - Flask 登录系统后端服务器
# ============================================================
# 这个文件包含完整的 Web 服务器逻辑
# 作为 Python 学习项目，每行代码都有详细中文注释
#
# 功能说明：
#   1. 提供 HTML 页面路由
#   2. 提供 API 接口处理登录请求
#   3. 连接 Neon PostgreSQL 数据库验证用户
#
# 作者：AI Assistant
# 日期：2025
# ============================================================

# ============================================================
# 第一部分：导入需要的模块
# ============================================================

# 导入 Flask 框架 - 这是 Python 最流行的轻量级 Web 框架
# Flask: 帮助我们快速创建 Web 服务器和处理 HTTP 请求
# 同时导入 send_from_directory 用于服务静态文件（CSS、JS）
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, send_from_directory

# 导入 CORS - 跨域资源共享
# 为什么需要：因为我们的前端和后端可能在不同端口运行
# 浏览器默认会阻止这种跨域请求，CORS 告助我们绕过这个限制
from flask_cors import CORS

# 导入环境变量加载工具
# 为什么需要：数据库密码等敏感信息不应该直接写在代码里
# 我们会把它们放在 .env 文件中，然后用这个工具加载
from dotenv import load_dotenv

# 导入操作系统模块
# 用途：读取环境变量（如数据库连接字符串）
import os

# 导入 PostgreSQL 数据库驱动
# psycopg2 是 Python 连接 PostgreSQL 数据库的标准库
import psycopg2
from psycopg2 import sql

# 导入时间模块
# 用途：记录操作时间
from datetime import datetime

# ============================================================
# 第二部分：创建 Flask 应用实例
# ============================================================

# 创建 Flask 应用实例
# __name__ 是 Python 的一个特殊变量
# 当这个文件被直接运行时，__name__ 的值是 '__main__'
# 当这个文件被其他文件导入时，__name__ 的值是这个模块的名字
app = Flask(__name__,
            static_folder='static')  # 指定 static 文件夹的位置

# ============================================================
# 第三部分：配置 Flask 应用
# ============================================================

# 设置 session 密钥
# Session 用于存储用户登录状态（类似浏览器的 Cookie）
# 密钥用于加密 session 数据，防止被篡改
# 注意：在生产环境中应该使用随机生成的复杂密钥
app.secret_key = 'dev-secret-key-change-in-production'

# 启用 CORS（跨域资源共享）
# 这样前端页面（可能在不同端口）就能调用后端 API
CORS(app)

# ============================================================
# 第四部分：加载数据库配置
# ============================================================

# 加载 .env 文件中的环境变量
# .env 文件内容示例：
#   DATABASE_URL="postgresql://user:pass@host/dbname"
load_dotenv()

# 从环境变量中获取数据库连接字符串
# DATABASE_URL 是我们在 .env 文件中定义的变量名
database_url = os.getenv('DATABASE_URL')

# 打印连接信息（调试用）
# 前面的 >>> 是 Python 控制台的输出提示符
print(f'>>> 准备连接数据库: {database_url}')

# ============================================================
# 第五部分：定义数据库连接函数
# ============================================================

def get_db_connection():
    """
    获取数据库连接
    返回：psycopg2 连接对象

    为什么用函数：每次请求都需要新的数据库连接
    这样可以避免连接超时的问题
    """
    # connect() 函数创建到数据库的连接
    # psycopg2 自动处理 SSL（安全连接）
    conn = psycopg2.connect(database_url)
    return conn

# ============================================================
# 第六部分：定义辅助函数
# ============================================================

def is_logged_in():
    """
    检查用户是否已登录
    返回：True（已登录）或 False（未登录）

    session 是 Flask 提供的字典，用于存储用户数据
    当用户登录成功，我们把用户名存入 session
    后续请求就能通过 session 识别用户身份
    """
    # 'user_id' 是我们在登录时存入 session 的键
    # 如果 session 中有这个键，说明用户已经登录
    return 'user_id' in session

# ============================================================
# 第七部分：定义路由（页面和 API）
# ============================================================

# ------------------------------------------------------------
# 路由 1：首页 - 自动判断跳转
# ------------------------------------------------------------
# 当用户访问 http://localhost:5000/ 时触发
# 这里的 '/' 代表网站的根路径
@app.route('/')
def index():
    """
    首页路由函数
    功能：根据登录状态跳转到不同页面
      - 已登录：跳转到 home.html（显示 Hello World）
      - 未登录：显示 login.html（登录页面）
    """
    # 检查用户登录状态
    if is_logged_in():
        # 如果已登录，重定向到 home 页面
        # url_for('home') 生成 home 路由的 URL
        return redirect(url_for('home'))
    else:
        # 如果未登录，显示登录页面
        # render_template() 函数渲染 templates 目录下的 HTML 文件
        return render_template('login.html')

# ------------------------------------------------------------
# 路由 2：登录页面（显示 HTML）
# ------------------------------------------------------------
# URL: http://localhost:5000/login
@app.route('/login')
def login_page():
    """
    显示登录页面
    功能：渲染 templates/login.html
    """
    return render_template('login.html')

# ------------------------------------------------------------
# 路由 3：Home 页面（登录后显示）
# ------------------------------------------------------------
# URL: http://localhost:5000/home
@app.route('/home')
def home():
    """
    Home 页面
    功能：显示 "Hello World!" 和用户名
    保护：未登录用户会自动跳转到登录页
    """
    # 如果用户未登录，跳转到登录页面
    if not is_logged_in():
        return redirect(url_for('login_page'))

    # 从 session 中获取用户名
    # session['username'] 是登录时存入的用户名
    username = session.get('username', '访客')

    # 渲染 home.html，传入用户名变量
    # 这样 HTML 模板就能使用 {{ username }} 显示用户名
    return render_template('home.html', username=username)

# ------------------------------------------------------------
# 路由 4：API - 登录验证
# ------------------------------------------------------------
# URL: http://localhost:5000/api/login
# methods=['POST'] 表示这个路由只响应 POST 请求（不是 GET）
@app.route('/api/login', methods=['POST'])
def api_login():
    """
    登录 API 接口
    请求格式：JSON
        {
            "username": "用户名",
            "password": "密码"
        }
    返回格式：JSON
        成功: {"success": true, "message": "登录成功", "username": "..."}
        失败: {"success": false, "message": "错误信息"}
    """
    try:
        # 获取前端发送的 JSON 数据
        # request 是 Flask 提供的对象，包含所有请求信息
        # get_json() 把请求体解析成 Python 字典
        data = request.get_json()

        # 从字典中提取用户名和密码
        username = data.get('username')
        password = data.get('password')

        # 打印调试信息（方便开发时查看）
        print(f'>>> 登录尝试: 用户名={username}')

        # ========================================================
        # 数据库查询部分
        # ========================================================

        # 获取数据库连接
        conn = get_db_connection()

        # 创建游标（Cursor）
        # 游标是执行 SQL 命令和获取结果的对象
        # 可以把它想象成数据库的"操作手"
        cursor = conn.cursor()

        # 执行 SQL 查询
        # %s 是占位符，会被后面的值替换
        # 这样可以防止 SQL 注入攻击（安全问题）
        # 我们查询的用户名和密码都要匹配
        query = "SELECT id, username FROM users WHERE username = %s AND password = %s"

        # execute() 执行 SQL 命令
        # 第二个参数是替换占位符的值（用元组传递）
        cursor.execute(query, (username, password))

        # fetchone() 获取查询结果
        # 如果有匹配的记录，返回包含用户信息的元组
        # 如果没有匹配，返回 None
        user = cursor.fetchone()

        # 关闭游标（释放资源）
        cursor.close()

        # 关闭数据库连接
        conn.close()

        # ========================================================
        # 验证结果处理
        # ========================================================

        if user:
            # 用户名和密码匹配 - 登录成功！

            # user 是一个元组，格式是 (id, username)
            # user[0] 是 id，user[1] 是 username
            user_id = user[0]
            user_name = user[1]

            # 把用户信息存入 session
            # session 是服务器端的存储，可以安全地保存用户数据
            session['user_id'] = user_id
            session['username'] = user_name

            # 打印成功日志
            print(f'>>> 登录成功: {user_name} (ID: {user_id})')

            # 返回成功响应给前端
            # jsonify() 把 Python 字典转换成 JSON 格式
            return jsonify({
                'success': True,
                'message': '登录成功！',
                'username': user_name
            })
        else:
            # 用户名或密码错误 - 登录失败

            # 打印失败日志
            print(f'>>> 登录失败: 用户名或密码错误')

            # 返回失败响应
            # HTTP 状态码 401 表示"未授权"
            return jsonify({
                'success': False,
                'message': '用户名或密码错误，请重试'
            }), 401

    except Exception as e:
        # 捕获任何异常（数据库连接失败、数据格式错误等）

        # 打印错误信息
        print(f'>>> 登录错误: {str(e)}')

        # 返回服务器错误响应
        # HTTP 状态码 500 表示"服务器内部错误"
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500

# ------------------------------------------------------------
# 路由 5：API - 检查登录状态
# ------------------------------------------------------------
# URL: http://localhost:5000/api/check
# methods=['GET'] 表示只响应 GET 请求
@app.route('/api/check', methods=['GET'])
def api_check():
    """
    检查登录状态 API
    返回：JSON
        已登录: {"logged_in": true, "username": "..."}
        未登录: {"logged_in": false}
    """
    # 检查用户是否已登录
    if is_logged_in():
        # 已登录
        return jsonify({
            'logged_in': True,
            'username': session.get('username')
        })
    else:
        # 未登录
        return jsonify({'logged_in': False})

# ------------------------------------------------------------
# 路由 6：API - 登出
# ------------------------------------------------------------
# URL: http://localhost:5000/api/logout
# methods=['POST'] 表示只响应 POST 请求
@app.route('/api/logout', methods=['POST'])
def api_logout():
    """
    登出 API
    功能：清除用户 session
    返回：JSON {"success": true, "message": "已登出"}
    """
    # 清除 session 中的所有数据
    # 这样用户就变成了"未登录"状态
    session.clear()

    # 打印登出日志
    print('>>> 用户已登出')

    # 返回成功响应
    return jsonify({
        'success': True,
        'message': '已成功登出'
    })

# ------------------------------------------------------------
# 路由 7：测试 API - 验证数据库连接
# ------------------------------------------------------------
# URL: http://localhost:5000/api/test-db
# 这个路由仅用于开发调试，测试数据库是否正常连接
@app.route('/api/test-db')
def test_database():
    """
    数据库测试接口
    功能：尝试连接数据库并执行简单查询
    返回：数据库状态信息
    """
    try:
        # 获取数据库连接
        conn = get_db_connection()

        # 创建游标
        cursor = conn.cursor()

        # 执行简单查询：计算用户表中有多少个用户
        cursor.execute('SELECT COUNT(*) FROM users')

        # 获取结果
        count = cursor.fetchone()[0]

        # 关闭游标和连接
        cursor.close()
        conn.close()

        # 返回成功信息
        return jsonify({
            'success': True,
            'message': '数据库连接正常',
            'user_count': count
        })

    except Exception as e:
        # 连接失败，返回错误信息
        return jsonify({
            'success': False,
            'message': f'数据库连接失败: {str(e)}'
        }), 500

# ============================================================
# 第八部分：错误处理
# ============================================================

# 定义 404 错误处理函数
# 当用户访问不存在的页面时触发
@app.errorhandler(404)
def page_not_found(e):
    """
    404 错误页面
    当访问的 URL 不存在时显示
    """
    return jsonify({
        'success': False,
        'message': '页面不存在'
    }), 404

# ============================================================
# 第九部分：启劝服务器
# ============================================================

# 这是 Python 的标准写法
# __name__ == '__main__' 表示这个文件被直接运行
# 而不是被其他文件导入
if __name__ == '__main__':
    # 打印启动信息
    print('=' * 50)
    print('>>> Flask 服务器正在启动...')
    print(f'>>> 访问地址: http://localhost:5000')
    print(f'>>> 登录页面: http://localhost:5000/login')
    print('=' * 50)

    # run() 函数启劝 Flask 开发服务器
    # debug=True 启用调试模式（代码修改会自动重新加载）
    # port=5000 指定端口号为 5000
    app.run(debug=True, port=5000)

# ============================================================
# 代码结束
# ============================================================
# 运行方式：在终端执行 python app.py
# 然后在浏览器访问 http://localhost:5000
# ============================================================
