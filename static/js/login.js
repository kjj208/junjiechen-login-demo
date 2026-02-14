// Vue.js 登录页面逻辑
// 这个文件包含登录页面的所有交互逻辑
// 使用 Vue 3 的 Options API 风格编写

const { createApp } = Vue;

createApp({
    // data() 函数定义组件的数据（状态）
    // Vue 会把这些数据变成"响应式"的
    // 当数据改变时，UI 会自动更新
    data() {
        return {
            // username - 用户输入的用户名
            username: '',

            // password - 用户输入的密码
            password: '',

            // loading - 登录请求的加载状态
            // true: 正在请求中，按钮禁用并显示加载动画
            // false: 请求完成或失败，按钮可用
            loading: false,

            // message - 显示给用户的消息
            // null: 不显示消息
            // { text: '消息文本', type: 'error'或'success' }: 显示消息
            message: null
        };
    },

    // methods 对象包含所有自定义函数
    methods: {
        // showMessage - 显示消息框
        // text: 消息文本
        // type: 'error'（红色）或 'success'（绿色）
        showMessage(text, type) {
            const box = document.getElementById('message-box');
            box.textContent = text;
            box.className = 'message ' + type;
            box.style.display = 'block';
        },

        // hideMessage - 隐藏消息框
        hideMessage() {
            const box = document.getElementById('message-box');
            box.style.display = 'none';
        },

        // handleLogin - 处理登逻辑（异步函数）
        async handleLogin(e) {
            // 阻止表单默认提交行为（否则页面会刷新）
            e.preventDefault();

            // 清空之前的消息
            this.hideMessage();

            // 获取用户输入
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // 基本验证：检查用户名和密码是否为空
            if (!username || !password) {
                this.showMessage('请输入用户名和密码', 'error');
                return;
            }

            // 设置加载状态为 true
            this.loading = true;

            // 获取按钮元素并更新状态
            const btn = document.getElementById('login-btn');
            btn.disabled = true;
            btn.innerHTML = '<span class="loading"></span>登录中...';

            try {
                // 使用 fetch API 发送 POST 请求到后端
                // fetch 是浏览器内置的 HTTP 请求函数
                const response = await fetch('/api/login', {
                    method: 'POST',              // 请求方法：POST
                    headers: {
                        // 告诉请求体是 JSON 格式
                        'Content-Type': 'application/json'
                    },
                    // 把用户名和密码打包成 JSON 字符串发送
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });

                // 解析响应体为 JavaScript 对象
                const data = await response.json();

                // 检查响应结果
                if (data.success) {
                    // 登录成功！
                    this.showMessage(data.message, 'success');

                    // 等待 500 毫秒后跳转到 home 页面
                    setTimeout(() => {
                        window.location.href = '/home';
                    }, 500);
                } else {
                    // 登录失败（用户名或密码错误）
                    this.showMessage(data.message || '登录失败，请重试', 'error');
                }
            } catch (error) {
                // 网络错误或服务器错误
                this.showMessage('网络错误，请稍后重试', 'error');
                console.error('Login error:', error);
            } finally {
                // 无论成功还是失败，都要重置加载状态
                this.loading = false;
                btn.disabled = false;
                btn.textContent = '登录';
            }
        }
    },

    // mounted - Vue 组件已挂载到 DOM
    // 在这里添加事件监听器
    mounted() {
        const form = document.getElementById('login-form');
        form.addEventListener('submit', this.handleLogin);
    },

    // beforeUnmount - Vue 组件即将卸载
    // 在这里移除事件监听器，防止内存泄漏
    beforeUnmount() {
        const form = document.getElementById('login-form');
        form.removeEventListener('submit', this.handleLogin);
    }
});

// 把 Vue 应用挂载到 id="app" 的 HTML 元素上
// 这会启动 Vue 应用，开始管理这个 DOM 区域
Vue.createApp({}).mount('#app');
