"""
对话管理服务
"""
from app.models.dialogue import DialogueContext, Message
from app.models.state import EmotionalState, Scenario
from app.services.model_a import model_a_service
from app.services.model_b import model_b_service
from app.prompts.model_a_prompts import SCENARIO_FIRST_MEET


class DialogueManager:
    """对话管理器"""
    
    def __init__(self):
        self.context: DialogueContext | None = None
        self.current_scenario: dict | None = None
        self.emotional_states: list[EmotionalState] = []
        self.current_state: EmotionalState | None = None
    
    def start_new_dialogue(self, scenario_id: str = "first_meet"):
        """
        开始新对话
        
        Args:
            scenario_id: 情境 ID
        """
        # 加载情境（MVP 阶段只有一个情境）
        self.current_scenario = SCENARIO_FIRST_MEET
        
        # 初始化对话上下文
        self.context = DialogueContext(scenario_id=scenario_id)
        
        # 初始化情绪状态
        initial_state = EmotionalState(
            valence=0.0,
            arousal=0.0,
            trust=0.5,
            openness=0.4,
            distance=0.6
        )
        self.current_state = initial_state
        self.emotional_states = [initial_state]
    
    async def process_user_input(self, user_input: str) -> str:
        """
        处理用户输入并生成回复
        
        Args:
            user_input: 用户输入
        
        Returns:
            AI 回复
        """
        if not self.context or not self.current_state:
            raise ValueError("对话未初始化，请先调用 start_new_dialogue()")
        
        # 添加用户消息
        self.context.add_message("user", user_input)
        
        # 准备消息历史（不包含 system）
        messages = self.context.to_openai_format(include_system=False)
        
        # 调用 Model A 生成回复
        response, updated_state = await model_a_service.generate_response(
            messages=messages,
            scenario=self.current_scenario,
            emotional_state=self.current_state
        )
        
        # 更新状态
        self.current_state = updated_state
        self.emotional_states.append(updated_state)
        
        # 添加 AI 回复
        self.context.add_message("assistant", response)
        
        return response
    
    async def get_analysis(self, recent_turns: int = 5) -> str:
        """
        获取对话分析
        
        Args:
            recent_turns: 分析最近几轮
        
        Returns:
            分析结果
        """
        if not self.context:
            raise ValueError("对话未初始化")
        
        analysis = await model_b_service.analyze_dialogue(
            context=self.context,
            emotional_states=self.emotional_states,
            recent_turns=recent_turns
        )
        
        return analysis
    
    def get_dialogue_summary(self) -> dict:
        """获取对话摘要（用于调试）"""
        if not self.context or not self.current_state:
            return {}
        
        return {
            "total_turns": len(self.context.messages) // 2,
            "current_emotion": self.current_state._get_emotion_description(),
            "current_relation": self.current_state._get_relation_description()
        }


dialogue_manager = DialogueManager()