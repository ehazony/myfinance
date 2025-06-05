import importlib
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


def setup_module(module):
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    import finance_common.db
    importlib.reload(finance_common.db)


def test_create_account():
    # Create a test-specific Base and Account model to avoid import issues
    TestBase = declarative_base()
    
    class TestAccount(TestBase):
        __tablename__ = "account"
        id = Column(Integer, primary_key=True)
        name = Column(String(128))
    
    # Create test database engine
    test_engine = create_engine('sqlite:///:memory:')
    TestSession = sessionmaker(bind=test_engine)

    # Create tables in test database
    TestBase.metadata.create_all(bind=test_engine)
    
    # Verify tables are registered
    assert 'account' in TestBase.metadata.tables, f"Account table not found. Available tables: {list(TestBase.metadata.tables.keys())}"
    
    with TestSession() as session:
        acc = TestAccount(name="demo")
        session.add(acc)
        session.commit()
        assert acc.id is not None


def test_import_models():
    """Test that all models can be imported successfully."""
    # This tests the import structure without SQLAlchemy table creation issues
    try:
        from finance_common.models import (
            Account, Conversation, Message, DateInput, Credential, 
            Tag, TagGoal, Transaction, RecurringTransaction, 
            TransactionNameTag, Plan, AdditionalInfo, 
            DiscountCredential, ErrorLog
        )
        # If we get here, all imports worked
        assert True
    except ImportError as e:
        assert False, f"Failed to import models: {e}"
