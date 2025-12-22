"""
Model B 对话分析服务
"""
from app.core.llm_client import llm_client
from app.core.config import settings
from app.models.dialogue import DialogueContext
from app.models.state import EmotionalState
from app.prompts.model_b_prompts import ANALYSIS_SYSTEM_PROMPT, build_analysis_prompt


class ModelBService:
    """对话分析模型服务"""
    
    def __init__(self):
        self.model_name = settings.MODEL_B_NAME
        self.temperature = settings.MODEL_B_TEMPERATURE
        self.max_tokens = settings.MODEL_B_MAX_TOKENS
    
    async def analyze_dialogue(
        self,
        context: DialogueContext,
        emotional_states: list[EmotionalState],
        recent_turns: int = 5
    ) -> str:
        """
        分析对话表现
        
        Args:
            context: 对话上下文
            emotional_states: 情绪状态历史
            recent_turns: 分析最近几轮对话
        
        Returns:
            分析结果
        """
        # 获取最近的对话
        recent_messages = context.get_recent_messages(recent_turns * 2)
        
        # 构建对话历史文本
        dialogue_text = self._format_dialogue_history(recent_messages)
        
        # 构建情绪轨迹描述
        emotional_trajectory = self._format_emotional_trajectory(emotional_states)
        
        # 构建分析 prompt
        analysis_prompt = build_analysis_prompt(dialogue_text, emotional_trajectory)
        
        # 调用 LLM
        messages = [
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": analysis_prompt}
        ]
        
        analysis = await llm_client.chat_completion(
            messages=messages,
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return analysis
    
    def _format_dialogue_history(self, messages: list) -> str:
        """格式化对话历史"""
        lines = []
        for msg in messages:
            if msg.role == "user":
                lines.append(f"用户：{msg.content}")
            elif msg.role == "assistant":
                lines.append(f"对方：{msg.content}")
        return "\n".join(lines)
    
    def _format_emotional_trajectory(self, states: list[EmotionalState]) -> str:
        """格式化情绪轨迹"""
        if not states:
            return "无情绪记录"
        
        trajectory = []
        for i, state in enumerate(states):
            desc = state._get_emotion_description()
            trajectory.append(f"第 {i+1} 轮后：{desc}")
        
        return "\n".join(trajectory)


model_b_service = ModelBService()