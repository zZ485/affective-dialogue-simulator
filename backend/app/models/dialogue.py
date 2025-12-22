"""
对话相关数据模型
"""
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class Message(BaseModel):
    """单条消息"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = datetime.now()


class DialogueContext(BaseModel):
    """对话上下文"""
    scenario_id: str  # 情境 ID
    messages: list[Message] = []
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        self.messages.append(Message(role=role, content=content))
    
    def get_recent_messages(self, n: int) -> list[Message]:
        """获取最近 n 条消息"""
        return self.messages[-n:] if len(self.messages) > n else self.messages
    
    def to_openai_format(self, include_system: bool = True) -> list[dict]:
        """转换为 OpenAI API 格式"""
        result = []
        for msg in self.messages:
            if not include_system and msg.role == "system":
                continue
            result.append({
                "role": msg.role,
                "content": msg.content
            })
        return result