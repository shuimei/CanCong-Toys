# CanCong-Toys - 实用小工具合集

一个基于 FastAPI 和 Vue.js 的实用小工具合集网站，提供各种在线小工具，方便快捷地解决日常问题。

## 功能特点

- 工具搜索功能
- 热门工具和最新工具展示
- 现代简洁的界面设计
- 卡片式交互动效
- 响应式布局，支持移动端使用

## 技术栈

- 后端：FastAPI + SQLite3
- 前端：Vue 3 + Element Plus
- 构建工具：Vite

## 快速开始

### 后端启动

1. 进入后端目录：
   ```
   cd backend
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 启动服务：
   ```
   python cli.py start
   ```

   或者使用 uvicorn：
   ```
   uvicorn main:app --reload
   ```

   后端服务将运行在 http://localhost:8000

### 前端启动

1. 进入前端目录：
   ```
   cd frontend
   ```

2. 安装依赖：
   ```
   npm install
   ```

3. 启动开发服务器：
   ```
   npm run dev
   ```

   前端服务将运行在 http://localhost:3001

### 自动启动脚本

为了简化启动过程，项目提供了自动启动脚本：

#### Windows系统
```
# 后端
scripts\service_manager.bat

# 前端
frontend\start.bat
```

#### Linux/macOS系统
```
# 给脚本添加执行权限
chmod +x scripts/service_manager.sh
chmod +x frontend/start.sh

# 后端
scripts/service_manager.sh

# 前端
frontend/start.sh
```

## 环境配置

项目使用环境变量来管理不同环境的配置。

### 后端环境配置

后端使用 `.env` 文件进行配置，可配置项包括：

- `APP_NAME`: 应用名称
- `DEBUG`: 调试模式开关
- `HOST`: 服务器监听地址
- `PORT`: 服务器监听端口
- `DATABASE_URL`: 数据库连接URL
- `CORS_ORIGINS`: CORS允许的源
- `CORS_CREDENTIALS`: 是否允许携带凭证
- `CORS_METHODS`: 允许的HTTP方法
- `CORS_HEADERS`: 允许的请求头

### 前端环境配置

前端使用以下环境配置文件：

- `.env`: 默认环境配置
- `.env.development`: 开发环境配置
- `.env.production`: 生产环境配置

可配置项包括：

- `VITE_API_BASE_URL`: API基础URL
- `VITE_APP_ENV`: 应用环境

## 服务管理

项目提供了多种方式管理服务：

### CLI命令行方式（推荐）

进入后端目录后，可以使用以下命令：

```
# 启动服务（前台）
python cli.py start

# 后台启动服务
python cli.py start --daemon

# 停止服务
python cli.py stop

# 重启服务
python cli.py restart

# 查看服务状态
python cli.py status

# 开发模式启动（带自动重载）
python cli.py dev
```

### 图形界面方式

#### Windows系统
```
scripts\service_manager.bat
```

#### Linux/macOS系统
```
chmod +x scripts/service_manager.sh
scripts/service_manager.sh
```

## 项目结构

```
CanCong-Toys/
├── backend/              # 后端代码
│   ├── app/              # 应用核心代码
│   │   ├── api/          # API路由
│   │   ├── tools/        # 工具功能实现
│   │   └── ...
│   ├── main.py           # 应用入口
│   ├── cli.py            # CLI管理工具
│   ├── requirements.txt  # Python依赖
│   └── .env              # 环境配置文件
├── frontend/             # 前端代码
│   ├── src/              # 源代码
│   │   ├── components/   # 组件
│   │   ├── views/        # 页面视图
│   │   ├── config/       # 配置文件
│   │   ├── App.vue       # 根组件
│   │   └── main.js       # 入口文件
│   ├── index.html        # HTML模板
│   ├── .env              # 默认环境配置
│   ├── .env.development  # 开发环境配置
│   ├── .env.production   # 生产环境配置
│   └── package.json      # npm依赖
├── scripts/              # 服务管理脚本
│   ├── service_manager.bat  # Windows服务管理脚本
│   └── service_manager.sh   # Linux/macOS服务管理脚本
└── README.md
```

## 配置文件说明

### 后端配置
后端配置文件位于 `backend/.env`，包含应用配置、服务器配置、数据库配置和CORS配置等。

### 前端配置
前端配置文件位于 `frontend/` 目录下：
- `.env`: 默认配置文件
- `.env.development`: 开发环境配置
- `.env.production`: 生产环境配置

前端API地址配置示例：
```
VITE_API_BASE_URL=http://localhost:8000
```

在生产环境中，可以配置为相对路径：
```
VITE_API_BASE_URL=/api
```

## 当前实现的工具

1. **BMI计算器** - 计算身体质量指数，评估体重是否健康
2. **图片格式转换器** - 支持多种图片格式相互转换
3. **密码生成器** - 生成安全的随机密码，可自定义长度和字符类型
4. **文本大小写转换** - 将文本转换为大写、小写或首字母大写格式
5. **时间戳转换器** - 将时间戳转换为可读日期，或将日期转换为时间戳
6. **单位换算器** - 支持长度、重量、温度等多种单位换算

## 开发计划

- 添加更多实用工具
- 实现用户收藏功能
- 增加工具使用统计
- 支持工具分类浏览
- 添加工具评分功能

## 许可证

MIT