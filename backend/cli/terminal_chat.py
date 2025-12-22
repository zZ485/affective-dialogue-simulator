"""
终端对话界面 - MVP 实现
"""
import sys
from pathlib import Path

# 动态添加 backend 目录到 Python 路径
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
import sys
from app.services.dialogue_manager import dialogue_manager


class TerminalChat:
    """终端对话界面"""
    
    def __init__(self):
        self.running = False
    
    async def start(self):
        """启动对话"""
        self.running = True
        
        # 显示欢迎信息
        self._print_welcome()
        
        # 初始化对话
        dialogue_manager.start_new_dialogue()
        
        # 主循环
        while self.running:
            try:
                # 获取用户输入
                user_input = await self._get_user_input()
                
                if not user_input:
                    continue
                
                # 处理特殊命令
                if self._handle_command(user_input):
                    continue
                
                # 发送给 Model A
                print("\n[对方正在输入...]\n")
                response = await dialogue_manager.process_user_input(user_input)
                
                # 显示回复
                self._print_response(response)
                
            except KeyboardInterrupt:
                print("\n\n检测到中断信号，正在退出...")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                import traceback
                traceback.print_exc()
    
    def _print_welcome(self):
        """打印欢迎信息"""
        print("=" * 60)
        print("🎭 情感对话能力训练系统 - MVP 版本")
        print("=" * 60)
        print("\n📖 使用说明：")
        print("  - 直接输入消息进行对话")
        print("  - 输入 /analyze 查看对话分析")
        print("  - 输入 /summary 查看当前状态（调试用）")
        print("  - 输入 /quit 或 Ctrl+C 退出")
        print("\n💡 提示：")
        print("  这是一个训练系统，对方不会永远理解你、迎合你")
        print("  观察对方的反应，尝试不同的表达方式")
        print("\n" + "=" * 60)
        print("\n🎬 情境：初次见面")
        print("你们刚通过朋友介绍认识，这是第一次线上聊天\n")
        print("-" * 60)
    
    async def _get_user_input(self) -> str:
        """获取用户输入"""
        try:
            # 使用异步方式获取输入
            loop = asyncio.get_event_loop()
            user_input = await loop.run_in_executor(
                None,
                lambda: input("\n你：")
            )
            return user_input.strip()
        except EOFError:
            return "/quit"
    
    def _handle_command(self, user_input: str) -> bool:
        """
        处理特殊命令
        
        Returns:
            是否为命令（True 则跳过正常对话流程）
        """
        if user_input.startswith("/"):
            command = user_input.lower()
            
            if command == "/quit":
                print("\n👋 感谢使用，再见！")
                self.running = False
                return True
            
            elif command == "/analyze":
                print("\n[正在分析对话...]\n")
                asyncio.create_task(self._show_analysis())
                return True
            
            elif command == "/summary":
                summary = dialogue_manager.get_dialogue_summary()
                print(f"\n📊 对话摘要：")
                print(f"  对话轮数：{summary.get('total_turns', 0)}")
                print(f"  情绪状态：{summary.get('current_emotion', '未知')}")
                print(f"  关系状态：{summary.get('current_relation', '未知')}")
                return True
            
            elif command.startswith("/help"):
                self._print_welcome()
                return True
            
            else:
                print(f"❌ 未知命令：{command}")
                return True
        
        return False
    
    async def _show_analysis(self):
        """显示对话分析"""
        try:
            analysis = await dialogue_manager.get_analysis(recent_turns=5)
            print("\n" + "=" * 60)
            print("📈 对话分析报告")
            print("=" * 60 + "\n")
            print(analysis)
            print("\n" + "=" * 60)
        except Exception as e:
            print(f"❌ 分析失败: {e}")
    
    def _print_response(self, response: str):
        """打印 AI 回复"""
        print(f"\n对方：{response}")
        print("-" * 60)


async def main():
    """主函数"""
    chat = TerminalChat()
    await chat.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
        sys.exit(0)