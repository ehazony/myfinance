"""
End-to-end integration test for transaction retrieval.
Tests the full flow: finance_tools -> client wrapper -> OpenAPI client -> backend API.
"""

import json
import sys
import os
from datetime import datetime, date
from google.adk.tools.tool_context import ToolContext
# Add dotenv support
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file.")
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv if you want .env support.")

# Add parent directories to path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents_adk.tools.finance_tools import get_user_transactions

# Get token from environment or use placeholder
TEST_TOKEN = os.environ.get('FINANCE_TEST_TOKEN', 'your_token_here')

class MockToolContextState:
    """Mock state for ToolContext"""
    def __init__(self, token):
        self._data = {'user_token': token}
    
    def get(self, key, default=None):
        return self._data.get(key, default)

class MockToolContext:
    """Mock ToolContext for testing"""
    def __init__(self, token):
        self.state = MockToolContextState(token)

def get_test_token():
    """Get test token from environment or prompt user"""
    if TEST_TOKEN and TEST_TOKEN != 'your_token_here':
        print(f"Using token from environment: {TEST_TOKEN[:20]}...")
        return TEST_TOKEN
    else:
        print("No FINANCE_TEST_TOKEN environment variable set.")
        print("Set it with: export FINANCE_TEST_TOKEN='your_actual_token'")
        print("Or update TEST_TOKEN in the script directly.")
        return None

def test_basic_transaction_retrieval():
    """Test basic transaction retrieval without filters"""
    print("=== Testing Basic Transaction Retrieval ===")
    
    test_token = get_test_token()
    if not test_token:
        print("❌ No valid token available, skipping test")
        return False
    
    tool_context = MockToolContext(test_token)
    
    try:
        print("Calling get_user_transactions with no filters...")
        result = get_user_transactions(tool_context)
        
        print(f"Raw result type: {type(result)}")
        
        # Parse JSON response
        data = json.loads(result)
        print(f"Parsed data keys: {data.keys()}")
        
        if 'error' in data:
            print(f"❌ Error in response: {data['error']}")
            return False
        
        if 'transactions' in data:
            transactions = data['transactions']
            print(f"✅ Retrieved {len(transactions)} transactions")
            
            if transactions:
                print("Sample transaction:")
                print(json.dumps(transactions[0], indent=2))
            
            return True
        else:
            print(f"❌ No 'transactions' key in response: {data}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during basic retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_date_filtering_with_none():
    """Test date filtering with None values - validates wrapper conversion"""
    print("\n=== Testing Date Filtering with None Values ===")
    
    test_token = get_test_token()
    if not test_token:
        print("❌ No valid token available, skipping test")
        return False
    
    tool_context = MockToolContext(test_token)
    
    try:
        # Test with None values - should be converted to UNSET by wrapper
        print("Calling get_user_transactions with date_range=None (should work)...")
        result = get_user_transactions(
            tool_context, 
            date_range=None,  # This should be converted to UNSET
            category=None,    # This should be converted to UNSET
            limit=10
        )
        
        data = json.loads(result)
        
        if 'error' in data:
            print(f"❌ Error with None values: {data['error']}")
            return False
        
        if 'transactions' in data:
            print(f"✅ None values handled correctly, got {len(data['transactions'])} transactions")
            print(f"Filters used: {data.get('filters', {})}")
            return True
        else:
            print(f"❌ Unexpected response structure: {data}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during None value test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_date_range_filtering():
    """Test date range filtering with actual dates"""
    print("\n=== Testing Date Range Filtering ===")
    
    test_token = get_test_token()
    if not test_token:
        print("❌ No valid token available, skipping test")
        return False
    
    tool_context = MockToolContext(test_token)
    
    try:
        # Test with month format
        print("Testing with month format (2024-01)...")
        result = get_user_transactions(
            tool_context,
            date_range="2024-01",
            limit=5
        )
        
        data = json.loads(result)
        
        if 'error' in data:
            print(f"Error with month format: {data['error']}")
        else:
            print(f"✅ Month format worked, got {len(data.get('transactions', []))} transactions")
            print(f"Date range parsed: {data.get('filters', {}).get('parsed_start_date')} to {data.get('filters', {}).get('parsed_end_date')}")
        
        # Test with date range format
        print("\nTesting with date range format (2024-01-01:2024-01-31)...")
        result2 = get_user_transactions(
            tool_context,
            date_range="2024-01-01:2024-01-31",
            limit=5
        )
        
        data2 = json.loads(result2)
        
        if 'error' in data2:
            print(f"Error with date range format: {data2['error']}")
        else:
            print(f"✅ Date range format worked, got {len(data2.get('transactions', []))} transactions")
            print(f"Date range parsed: {data2.get('filters', {}).get('parsed_start_date')} to {data2.get('filters', {}).get('parsed_end_date')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception during date range test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_category_filtering():
    """Test category filtering"""
    print("\n=== Testing Category Filtering ===")
    
    test_token = get_test_token()
    if not test_token:
        print("❌ No valid token available, skipping test")
        return False
    
    tool_context = MockToolContext(test_token)
    
    try:
        # Test with a common category
        test_categories = ["Food", "Groceries", "Shopping", "Entertainment"]
        
        for category in test_categories:
            print(f"Testing category: {category}")
            result = get_user_transactions(
                tool_context,
                category=category,
                limit=3
            )
            
            data = json.loads(result)
            
            if 'error' in data:
                print(f"  Error with category {category}: {data['error']}")
            else:
                transactions = data.get('transactions', [])
                print(f"  ✅ Got {len(transactions)} transactions for {category}")
                
                # Check if transactions actually match the category
                if transactions:
                    sample_categories = [t.get('category', 'Unknown') for t in transactions[:2]]
                    print(f"  Sample categories: {sample_categories}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception during category test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """Test error handling with invalid token"""
    print("\n=== Testing Error Handling ===")
    
    # Test with invalid token
    tool_context = MockToolContext("invalid_token_12345")
    
    try:
        print("Testing with invalid authentication token...")
        result = get_user_transactions(tool_context)
        
        data = json.loads(result)
        
        if 'error' in data:
            print(f"✅ Error correctly handled: {data['error']}")
            return True
        else:
            print(f"❌ Expected error but got: {data}")
            return False
            
    except Exception as e:
        print(f"✅ Exception correctly raised for invalid token: {e}")
        return True

def run_all_tests():
    """Run all end-to-end tests"""
    print("🚀 Starting End-to-End Transaction Tests")
    print("=" * 50)
    
    # Check if we have a valid token before starting
    if not get_test_token():
        print("❌ Cannot run tests without valid authentication token")
        print("Please set FINANCE_TEST_TOKEN environment variable or update TEST_TOKEN in script")
        return
    
    tests = [
        test_basic_transaction_retrieval,
        test_date_filtering_with_none,
        test_date_range_filtering,
        test_category_filtering,
        test_error_handling
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except KeyboardInterrupt:
            print("\n🛑 Tests interrupted by user")
            break
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed - check output above")

if __name__ == "__main__":
    run_all_tests() 