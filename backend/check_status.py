#!/usr/bin/env python3
"""
简单状态检查
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_structure():
    """检查项目结构"""
    print("📋 项目结构检查:")
    
    required_files = [
        "app/__init__.py",
        "app/main.py", 
        "app/core/__init__.py",
        "app/models/__init__.py",
        "app/prompts/__init__.py", 
        "app/services/__init__.py",
        "cli/__init__.py",
        "tests/__init__.py"
    ]
    
    for file_path in required_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"  ✅ {file_path} ({size} bytes)")
        else:
            print(f"  ❌ {file_path} (缺失)")

def test_basic_imports():
    """测试基础导入"""
    print("\n🔍 基础导入测试:")
    
    modules = [
        ("app.core", "settings"),
        ("app.models", "Message"),
        ("app.prompts", "SCENARIO_FIRST_MEET"),
        ("cli", "TerminalChatApp"),
        ("app.main", "create_app")
    ]
    
    for module, item in modules:
        try:
            exec(f"from {module} import {item}")
            print(f"  ✅ from {module} import {item}")
        except Exception as e:
            print(f"  ❌ from {module} import {item} - {e}")

if __name__ == "__main__":
    check_structure()
    test_basic_imports()