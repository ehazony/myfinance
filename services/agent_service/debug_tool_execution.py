#!/usr/bin/env python3
"""
Debug script to check tool execution without ADK framework
"""

import sys
import os
import asyncio
from typing import Optional

# Add necessary paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Simple mock ToolContext
class MockToolContext:
    def __init__(self, user_token: str):
        self.state = {
            'user_token': user_token,
            'token': user_token
        }

# Import the tool function
from agents_adk.tools.finance_tools import get_user_transactions

def test_direct_tool_call():
    """Test calling the tool directly without ADK framework"""
    print("🔧 Testing direct tool call...")
    
    # Mock tool context with a test token
    mock_context = MockToolContext("037e235af8b1ae28b4b1be5a7b9c6c4e1e7a15e8c92a4e5c2d1f6a8b3e9c7f1d2")
    
    # Test with no parameters (should work now)
    print("📞 Calling get_user_transactions() with no parameters...")
    try:
        result = get_user_transactions(tool_context=mock_context)
        print(f"✅ Tool result: {result[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Tool call failed: {e}")
        return False

def test_tool_signature():
    """Test that tool signature is correct"""
    print("🔍 Checking tool signature...")
    import inspect
    print(f"Inspecting get_user_transactions from module: {get_user_transactions.__module__}")
    sig = inspect.signature(get_user_transactions)
    print(f"📋 Function signature: {sig}")
    
    # Check each parameter
    for name, param in sig.parameters.items():
        print(f"  - {name}: {param}")
        if param.default == inspect.Parameter.empty:
            print(f"    ⚠️  {name} is REQUIRED")
        else:
            print(f"    ✅ {name} has default: {param.default}")

if __name__ == "__main__":
    print("🚀 Diagnostic: Tool Execution Debug")
    print("=" * 50)
    
    test_tool_signature()
    print()
    test_direct_tool_call() 