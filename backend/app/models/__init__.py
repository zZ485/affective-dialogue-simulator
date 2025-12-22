"""
数据模型模块

定义应用中使用的各种数据结构和状态管理。
"""

from .dialogue import Message, DialogueContext
from .state import EmotionalState, Scenario

__all__ = [
    "Message", 
    "DialogueContext", 
    "EmotionalState", 
    "Scenario"
]