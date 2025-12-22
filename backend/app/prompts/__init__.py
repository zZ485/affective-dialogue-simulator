"""
提示词模板模块

管理用于不同模型的提示词模板，确保角色一致性。
"""

from .model_a_prompts import SCENARIO_FIRST_MEET, build_model_a_system_prompt
from .model_b_prompts import ANALYSIS_SYSTEM_PROMPT, build_analysis_prompt

__all__ = [
    "SCENARIO_FIRST_MEET",
    "build_model_a_system_prompt", 
    "ANALYSIS_SYSTEM_PROMPT",
    "build_analysis_prompt"
]