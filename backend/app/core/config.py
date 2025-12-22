"""
核心配置管理
"""
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """应用配置"""
    
    # API 配置
    AIHUBMIX_API_KEY: str
    AIHUBMIX_BASE_URL: str = "https://api.aihubmix.com/v1"
    
    # 模型配置
    MODEL_A_NAME: str = "claude-3-5-sonnet-20241022"  # 情感模拟模型
    MODEL_B_NAME: str = "claude-3-5-sonnet-20241022"  # 分析模型
    MODEL_A_TEMPERATURE: float = 0.8
    MODEL_B_TEMPERATURE: float = 0.3
    MODEL_A_MAX_TOKENS: int = 800
    MODEL_B_MAX_TOKENS: int = 2000
    
    # 对话配置
    MAX_CONTEXT_TURNS: int = 10  # 最大上下文轮数
    
    # 开发配置
    DEBUG: bool = False
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()