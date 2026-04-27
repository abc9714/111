# README.md

# 千问智能助手 - 基于阿里云通义千问的Web聊天机器人

一个极简的Web聊天机器人，使用FastAPI后端调用阿里云通义千问大模型，前端提供友好的对话界面。

## ✨ 功能特点

- 🤖 基于阿里云通义千问大模型（qwen-turbo/plus/max）
- 💬 支持多轮对话，自动维护上下文
- 🎨 现代化的聊天界面，消息气泡样式
- ⚡ 异步请求，流畅的用户体验
- 🔧 简单的配置，开箱即用

## 📁 项目结构
customer-service-bot/
├── app.py # FastAPI后端服务
├── static/
│ └── index.html # 前端聊天界面
├── requirements.txt # Python依赖
└── README.md # 项目说明

## 🚀 快速开始

### 1. 获取阿里云API Key

访问[阿里云百炼平台](https://bailian.console.aliyun.com/)，开通“通义千问”服务，获取`DASHSCOPE_API_KEY`。

### 2. 配置环境变量

在终端中设置环境变量（或创建`.env`文件）：

```bash
# Linux / macOS
export DASHSCOPE_API_KEY="your-api-key-here"
export MODEL_NAME="qwen-turbo"  # 可选：qwen-turbo, qwen-plus, qwen-max

# Windows (CMD)
set DASHSCOPE_API_KEY=your-api-key-here
set MODEL_NAME=qwen-turbo

# Windows (PowerShell)
$env:DASHSCOPE_API_KEY="your-api-key-here"
$env:MODEL_NAME="qwen-turbo"