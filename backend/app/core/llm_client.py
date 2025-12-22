"""
LLM 调用客户端封装
"""
import httpx
from typing import Optional
from app.core.config import settings


class LLMClient:
    """LLM 调用客户端"""
    
    def __init__(self):
        self.base_url = settings.AIHUBMIX_BASE_URL
        self.api_key = settings.AIHUBMIX_API_KEY
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def chat_completion(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ) -> str:
        """
        调用聊天补全 API
        
        Args:
            messages: 消息列表（OpenAI 格式）
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大 token 数
            stream: 是否流式输出
        
        Returns:
            模型回复内容
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
        
        except httpx.HTTPError as e:
            print(f"HTTP 错误: {e}")
            raise
        except Exception as e:
            print(f"调用 LLM 时出错: {e}")
            raise
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()


# 全局单例
llm_client = LLMClient()