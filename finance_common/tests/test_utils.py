"""Tests for finance_common utilities."""

import pytest
import json

from finance_common.utils import (
    CompanyConstants,
    TagConstants,
    MessageConstants,
    validate_credential_json,
    generate_user_code,
    get_company_type,
    validate_tag_type,
    validate_message_sender,
    validate_message_content_type,
    format_transaction_identifier,
)


class TestCompanyConstants:
    """Test company-related constants."""
    
    def test_company_choices(self):
        assert CompanyConstants.DISCOUNT == 'DISCOUNT'
        assert CompanyConstants.CAL == 'CAL'
        assert CompanyConstants.MAX == 'MAX'
    
    def test_account_types(self):
        assert CompanyConstants.BANK == 'BANK'
        assert CompanyConstants.CARD == 'DEBIT_CARD'
    
    def test_company_type_mapping(self):
        assert CompanyConstants.COMPANY_TYPE[CompanyConstants.CAL] == CompanyConstants.CARD
        assert CompanyConstants.COMPANY_TYPE[CompanyConstants.MAX] == CompanyConstants.CARD
        assert CompanyConstants.COMPANY_TYPE[CompanyConstants.DISCOUNT] == CompanyConstants.BANK


class TestTagConstants:
    """Test tag-related constants."""
    
    def test_tag_types(self):
        assert TagConstants.MONTHLY_FIXED == 'MONTHLY FIXED'
        assert TagConstants.PERIODIC == 'PERIODIC'
        assert TagConstants.CONTINUOUS == 'CONTINUOUS'


class TestMessageConstants:
    """Test message-related constants."""
    
    def test_sender_types(self):
        assert MessageConstants.USER == "user"
        assert MessageConstants.AGENT == "agent"
    
    def test_content_types(self):
        assert MessageConstants.TEXT == "text"
        assert MessageConstants.IMAGE == "image"
        assert MessageConstants.BUTTONS == "buttons"
        assert MessageConstants.CHART == "chart"


class TestCredentialValidation:
    """Test credential validation functions."""
    
    def test_validate_credential_json_with_string(self):
        json_str = '{"username": "test", "password": "secret"}'
        result = validate_credential_json(json_str)
        assert result == {"username": "test", "password": "secret"}
    
    def test_validate_credential_json_with_dict(self):
        data = {"username": "test", "password": "secret"}
        result = validate_credential_json(data)
        assert result == data
    
    def test_validate_credential_json_invalid(self):
        with pytest.raises(ValueError, match="Invalid credential JSON"):
            validate_credential_json("invalid json")


class TestUserCode:
    """Test user code generation."""
    
    def test_generate_user_code_range(self):
        code = generate_user_code()
        assert 10000 <= code <= 90000
    
    def test_generate_user_code_uniqueness(self):
        codes = [generate_user_code() for _ in range(100)]
        # Very unlikely to get duplicates with this range
        assert len(set(codes)) > 90  # Allow for some possible collisions


class TestCompanyType:
    """Test company type validation."""
    
    def test_get_company_type_valid(self):
        assert get_company_type(CompanyConstants.DISCOUNT) == CompanyConstants.BANK
        assert get_company_type(CompanyConstants.CAL) == CompanyConstants.CARD
        assert get_company_type(CompanyConstants.MAX) == CompanyConstants.CARD
    
    def test_get_company_type_invalid(self):
        with pytest.raises(ValueError, match="Unknown company"):
            get_company_type("INVALID_COMPANY")


class TestTagValidation:
    """Test tag validation functions."""
    
    def test_validate_tag_type_valid(self):
        assert validate_tag_type(TagConstants.MONTHLY_FIXED) is True
        assert validate_tag_type(TagConstants.PERIODIC) is True
        assert validate_tag_type(TagConstants.CONTINUOUS) is True
    
    def test_validate_tag_type_invalid(self):
        assert validate_tag_type("INVALID_TYPE") is False


class TestMessageValidation:
    """Test message validation functions."""
    
    def test_validate_message_sender_valid(self):
        assert validate_message_sender(MessageConstants.USER) is True
        assert validate_message_sender(MessageConstants.AGENT) is True
    
    def test_validate_message_sender_invalid(self):
        assert validate_message_sender("invalid_sender") is False
    
    def test_validate_message_content_type_valid(self):
        assert validate_message_content_type(MessageConstants.TEXT) is True
        assert validate_message_content_type(MessageConstants.IMAGE) is True
        assert validate_message_content_type(MessageConstants.BUTTONS) is True
        assert validate_message_content_type(MessageConstants.CHART) is True
    
    def test_validate_message_content_type_invalid(self):
        assert validate_message_content_type("invalid_type") is False


class TestTransactionIdentifier:
    """Test transaction identifier formatting."""
    
    def test_format_transaction_identifier(self):
        result = format_transaction_identifier("Test Transaction", "2023-12-01", 123.45)
        assert result == "Test_Transaction_2023-12-01_123.45"
    
    def test_format_transaction_identifier_negative_value(self):
        result = format_transaction_identifier("Test", "2023-12-01", -50.0)
        assert result == "Test_2023-12-01_50.00"
    
    def test_format_transaction_identifier_long_name(self):
        long_name = "A" * 100
        result = format_transaction_identifier(long_name, "2023-12-01", 10.0)
        assert len(result) <= 64
        assert result.endswith("_2023-12-01_10.00") 