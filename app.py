# app.py
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from openai import AsyncOpenAI
from dotenv import load_dotenv

# 加载 .env 文件（如果存在）
load_dotenv()

# 检查必需的环境变量
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    print("=" * 60)
    print("❌ 错误：未找到 DASHSCOPE_API_KEY 环境变量。")
    print("请按以下步骤设置：")
    print("1. 在项目根目录创建 .env 文件，内容如下：")
    print("   DASHSCOPE_API_KEY=你的阿里云API密钥")
    print("2. 或者直接设置系统环境变量后再运行。")
    print(
        "获取 API Key：https://help.aliyun.com/zh/dashscope/developer-reference/acquisition-and-configuration-of-api-key")
    print("=" * 60)
    sys.exit(1)

MODEL_NAME = os.getenv("MODEL_NAME", "qwen-turbo")  # 可选 qwen-plus, qwen-max, qwen-turbo

# 初始化阿里云百炼客户端（兼容OpenAI接口）
client = AsyncOpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 初始化FastAPI应用
app = FastAPI(title="千问聊天机器人API", description="基于阿里千问大模型的聊天接口")

# 配置CORS，允许前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 定义请求和响应的数据模型
class ChatMessage(BaseModel):
    role: str  # system, user, assistant
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    role: str
    content: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """
    接收前端消息列表，调用千问大模型生成回复
    """
    try:
        # 将Pydantic模型转换为字典列表供OpenAI使用
        messages = [msg.dict() for msg in chat_request.messages]

        # 调用千问大模型
        completion = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            top_p=0.8,
        )

        reply = completion.choices[0].message.content
        return ChatResponse(role="assistant", content=reply)

    except Exception as e:
        # 将错误信息返回前端
        raise HTTPException(status_code=500, detail=f"大模型调用失败: {str(e)}")


# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")


# 根路径返回聊天界面
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("🚀 千问智能助手启动中...")
    print(f"📦 使用模型: {MODEL_NAME}")
    print(f"🌐 访问地址: http://127.0.0.1:8000")
    print("💡 按 Ctrl+C 停止服务")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000)