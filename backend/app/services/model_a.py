"""
Model A 情感模拟服务
"""
from app.core.llm_client import llm_client
from app.core.config import settings
from app.models.state import EmotionalState
from app.prompts.model_a_prompts import build_model_a_system_prompt


class ModelAService:
    """情感模拟模型服务"""
    
    def __init__(self):
        self.model_name = settings.MODEL_A_NAME
        self.temperature = settings.MODEL_A_TEMPERATURE
        self.max_tokens = settings.MODEL_A_MAX_TOKENS
    
    async def generate_response(
        self,
        messages: list[dict],
        scenario: dict,
        emotional_state: EmotionalState
    ) -> tuple[str, EmotionalState]:
        """
        生成情感化回复
        
        Args:
            messages: 对话历史（OpenAI 格式）
            scenario: 当前情境配置
            emotional_state: 当前情绪状态
        
        Returns:
            (回复内容, 更新后的情绪状态)
        """
        # 构建 system prompt
        state_desc = emotional_state.to_prompt_context()
        system_prompt = build_model_a_system_prompt(scenario, state_desc)
        
        # 准备完整消息
        full_messages = [
            {"role": "system", "content": system_prompt}
        ] + messages
        
        # 调用 LLM
        response = await llm_client.chat_completion(
            messages=full_messages,
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        # 简单的情绪状态更新逻辑（后续可以用 LLM 来推理）
        updated_state = self._update_emotional_state(
            emotional_state,
            messages[-1]["content"] if messages else "",
            response
        )
        
        return response, updated_state
    
    def _update_emotional_state(
        self,
        current_state: EmotionalState,
        user_message: str,
        ai_response: str
    ) -> EmotionalState:
        """
        根据交互更新情绪状态（简化版）
        
        这里使用启发式规则，后续可以改用 LLM 推理
        """
        new_state = current_state.model_copy(deep=True)
        
        # 简单的启发式判断
        user_lower = user_message.lower()
        
        # 负面信号
        if any(word in user_lower for word in ["为什么", "你怎么", "难道"]):
            new_state.update_from_interaction(
                delta_valence=-0.1,
                delta_trust=-0.05,
                delta_distance=0.05
            )
        
        # 正面信号
        elif any(word in user_lower for word in ["理解", "谢谢", "有意思", "同感"]):
            new_state.update_from_interaction(
                delta_valence=0.1,
                delta_trust=0.05,
                delta_openness=0.05,
                delta_distance=-0.05
            )
        
        return new_state


model_a_service = ModelAService()