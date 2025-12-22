"""
内部情绪与关系状态模型（对用户不可见）
"""
from pydantic import BaseModel, Field
from typing import Literal


class EmotionalState(BaseModel):
    """情绪状态（内部使用）"""
    
    # 情绪维度 (-1.0 到 1.0)
    valence: float = Field(default=0.0, ge=-1.0, le=1.0)  # 情绪效价（负面到正面）
    arousal: float = Field(default=0.0, ge=-1.0, le=1.0)  # 唤醒度（平静到激动）
    
    # 关系维度 (0.0 到 1.0)
    trust: float = Field(default=0.5, ge=0.0, le=1.0)      # 信任度
    openness: float = Field(default=0.5, ge=0.0, le=1.0)   # 开放度
    distance: float = Field(default=0.5, ge=0.0, le=1.0)   # 距离感（越高越疏远）
    
    def update_from_interaction(self, delta_valence: float = 0, 
                                delta_trust: float = 0,
                                delta_openness: float = 0,
                                delta_distance: float = 0):
        """根据交互更新状态"""
        self.valence = max(-1.0, min(1.0, self.valence + delta_valence))
        self.trust = max(0.0, min(1.0, self.trust + delta_trust))
        self.openness = max(0.0, min(1.0, self.openness + delta_openness))
        self.distance = max(0.0, min(1.0, self.distance + delta_distance))
    
    def to_prompt_context(self) -> str:
        """转换为 Prompt 上下文（供 Model A 使用）"""
        emotion_desc = self._get_emotion_description()
        relation_desc = self._get_relation_description()
        return f"当前情绪状态：{emotion_desc}\n当前关系状态：{relation_desc}"
    
    def _get_emotion_description(self) -> str:
        """获取情绪描述"""
        if self.valence > 0.3:
            mood = "心情不错"
        elif self.valence < -0.3:
            mood = "心情低落"
        else:
            mood = "情绪平稳"
        
        if self.arousal > 0.3:
            energy = "，较为激动"
        elif self.arousal < -0.3:
            energy = "，比较疲惫"
        else:
            energy = ""
        
        return mood + energy
    
    def _get_relation_description(self) -> str:
        """获取关系描述"""
        trust_level = "信任" if self.trust > 0.6 else "保持警惕" if self.trust < 0.4 else "谨慎"
        openness_level = "愿意分享" if self.openness > 0.6 else "有所保留" if self.openness < 0.4 else "适度交流"
        distance_level = "感觉疏远" if self.distance > 0.6 else "关系亲近" if self.distance < 0.4 else "保持适当距离"
        
        return f"{trust_level}，{openness_level}，{distance_level}"


class Scenario(BaseModel):
    """对话情境"""
    id: str
    name: str
    description: str
    initial_state: EmotionalState
    system_prompt: str  # 给 Model A 的角色设定