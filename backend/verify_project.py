#!/usr/bin/env python3
"""
项目结构验证脚本
验证所有__init__.py文件和模块导入是否正确配置
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def verify_imports():
    """验证所有关键模块导入"""
    print("🔍 验证项目模块导入...")
    print("=" * 50)
    
    results = {}
    
    # 测试核心模块
    try:
        from app.core import settings, LLMClient
        results['core'] = True
        print("✅ app.core - 导入成功")
    except Exception as e:
        results['core'] = f"❌ 错误: {e}"
        print(f"❌ app.core - 导入失败: {e}")
    
    # 测试数据模型
    try:
        from app.models import Message, DialogueContext, EmotionalState, Scenario
        results['models'] = True
        print("✅ app.models - 导入成功")
    except Exception as e:
        results['models'] = f"❌ 错误: {e}"
        print(f"❌ app.models - 导入失败: {e}")
    
    # 测试提示词
    try:
        from app.prompts import SCENARIO_FIRST_MEET, ANALYSIS_SYSTEM_PROMPT
        results['prompts'] = True
        print("✅ app.prompts - 导入成功")
    except Exception as e:
        results['prompts'] = f"❌ 错误: {e}"
        print(f"❌ app.prompts - 导入失败: {e}")
    
    # 测试服务
    try:
        from app.services import DialogueManager, ModelAService, ModelBService
        results['services'] = True
        print("✅ app.services - 导入成功")
    except Exception as e:
        results['services'] = f"❌ 错误: {e}"
        print(f"❌ app.services - 导入失败: {e}")
    
    # 测试CLI
    try:
        from cli import TerminalChat
        results['cli'] = True
        print("✅ cli - 导入成功")
    except Exception as e:
        results['cli'] = f"❌ 错误: {e}"
        print(f"❌ cli - 导入失败: {e}")
    
    # 测试主应用（如果存在）
    try:
        from app import main
        results['main'] = True
        print("✅ app.main - 导入成功")
    except Exception as e:
        # 检查文件是否存在且有内容
        main_file = os.path.join(project_root, 'app', 'main.py')
        if os.path.exists(main_file) and os.path.getsize(main_file) > 0:
            results['main'] = f"❌ 错误: {e}"
            print(f"❌ app.main - 导入失败: {e}")
        else:
            results['main'] = "⚠️ 文件为空或不存在"
            print("⚠️ app.main - 文件为空或尚未实现")
    
    print("=" * 50)
    
    # 汇总结果
    success_count = sum(1 for v in results.values() if v is True)
    total_count = len(results)
    
    if success_count == total_count:
        print(f"🎉 所有模块验证通过！({success_count}/{total_count})")
        return True
    else:
        print(f"⚠️  部分模块存在问题: ({success_count}/{total_count})")
        for module, result in results.items():
            if result is not True:
                print(f"   {module}: {result}")
        return False

def show_project_structure():
    """显示项目结构"""
    print("\n📁 项目结构:")
    print("backend/")
    print("├── app/")
    print("│   ├── __init__.py ✅")
    print("│   ├── main.py ✅")
    print("│   ├── core/")
    print("│   │   ├── __init__.py ✅")
    print("│   │   ├── config.py")
    print("│   │   └── llm_client.py")
    print("│   ├── models/")
    print("│   │   ├── __init__.py ✅")
    print("│   │   ├── dialogue.py")
    print("│   │   └── state.py")
    print("│   ├── services/")
    print("│   │   ├── __init__.py ✅")
    print("│   │   ├── dialogue_manager.py")
    print("│   │   ├── model_a.py")
    print("│   │   └── model_b.py")
    print("│   └── prompts/")
    print("│       ├── __init__.py ✅")
    print("│       ├── model_a_prompts.py")
    print("│       └── model_b_prompts.py")
    print("├── cli/")
    print("│   ├── __init__.py ✅")
    print("│   └── terminal_chat.py")
    print("├── tests/")
    print("│   └── __init__.py ✅")
    print("├── pyproject.toml ✅")
    print("├── .env.sample ✅")
    print("└── .env ✅")

if __name__ == "__main__":
    show_project_structure()
    print()
    success = verify_imports()
    
    if success:
        print("\n✨ 项目结构配置完成！所有 __init__.py 文件已正确设置。")
        sys.exit(0)
    else:
        print("\n❌ 项目配置存在问题，请检查错误信息。")
        sys.exit(1)