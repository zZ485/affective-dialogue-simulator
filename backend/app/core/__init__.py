"""
核心配置和工具模块

提供应用的基础配置、LLM客户端连接等核心功能。
"""

from .config import settings
from .llm_client import LLMClient

__all__ = ["settings", "LLMClient"]