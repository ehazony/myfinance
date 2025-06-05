#!/usr/bin/env python3
"""
Test script for the generated OpenAPI client.
"""

import asyncio
import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.finance_data_client import get_finance_client


async def test_generated_client():
    """Test the generated OpenAPI client integration."""
    
    print("🧪 Testing Generated OpenAPI Client")
    print("=" * 50)
    
    # Test with a dummy token (in real scenario this would be a valid user token)
    test_token = "test_token_123"
    
    try:
        client = get_finance_client()
        print("✅ Finance client initialized successfully")
        
        # Test 1: Get Financial Context
        print("\n📊 Testing financial context retrieval...")
        try:
            context = client.get_financial_context_sync(
                token=test_token,
                include_future_goals=True,
                limit_transactions=10
            )
            print(f"✅ Financial context retrieved: {len(str(context))} characters")
            print(f"   Keys: {list(context.keys()) if context else 'No data'}")
        except Exception as e:
            print(f"❌ Financial context failed: {e}")
        
        # Test 2: Get Account Summary
        print("\n💰 Testing account summary retrieval...")
        try:
            accounts = client.get_account_summary_sync(token=test_token)
            print(f"✅ Account summary retrieved: {len(accounts) if accounts else 0} accounts")
        except Exception as e:
            print(f"❌ Account summary failed: {e}")
        
        # Test 3: Get Transactions
        print("\n📋 Testing transaction retrieval...")
        try:
            transactions = client.get_filtered_transactions_sync(
                token=test_token,
                limit=5
            )
            print(f"✅ Transactions retrieved: {len(transactions) if transactions else 0} transactions")
        except Exception as e:
            print(f"❌ Transactions failed: {e}")
        
        # Test 4: Get Budget Analysis
        print("\n📈 Testing budget analysis...")
        try:
            budget = client.get_budget_analysis_sync(
                token=test_token,
                period="current_month"
            )
            print(f"✅ Budget analysis retrieved: {len(budget) if budget else 0} budget items")
        except Exception as e:
            print(f"❌ Budget analysis failed: {e}")
        
        # Test 5: Test Finance Tools Integration
        print("\n🔧 Testing finance tools integration...")
        try:
            from agents_adk.tools.finance_tools import get_user_transactions, get_user_account_summary
            
            # Test finance tools
            transactions_result = get_user_transactions(test_token, limit=3)
            print(f"✅ Finance tools transactions: {len(transactions_result)} characters")
            
            summary_result = get_user_account_summary(test_token)
            print(f"✅ Finance tools summary: {len(summary_result)} characters")
            
        except Exception as e:
            print(f"❌ Finance tools integration failed: {e}")
            # This is expected since we don't have a running Django server
            print("   (This is expected without a running Django server with valid authentication)")
        
        print("\n" + "=" * 50)
        print("🎉 OpenAPI Client Test Complete!")
        print("📝 Note: 401 errors are expected without a running Django server and valid tokens")
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_generated_client()) 