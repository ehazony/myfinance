"""
Shared utilities and constants for the finance application.
"""
import json
import random
from typing import Dict, Any, Optional


class CompanyConstants:
    """Constants for financial institutions and card types."""
    
    # Company choices
    DISCOUNT = 'DISCOUNT'
    CAL = 'CAL'
    MAX = 'MAX'
    
    # Account types
    BANK = 'BANK' 
    CARD = 'DEBIT_CARD'
    
    # Additional info keys
    ADDITIONAL_INFO_BALANCE = 'balance'
    ADDITIONAL_INFO_LOANS = 'loans'
    
    COMPANY_CHOICES = (
        (DISCOUNT, "Discount"),
        (CAL, "Cal"),
        (MAX, "Max"),
    )
    
    TYPE_CHOICES = (
        (BANK, 'Bank'),
        (CARD, 'Debit Card'),
    )
    
    COMPANY_TYPE = {
        CAL: CARD,
        MAX: CARD,
        DISCOUNT: BANK
    }
    
    COMPANY_CHOICES_WITH_FIELDS = [
        {
            'key': DISCOUNT, 'name': 'Discount',
            'fields': [
                {'key': 'username', 'name': 'User Name', 'type': 'text'},
                {'key': 'password', 'name': 'Password', 'type': 'password'}
            ],
        },
        {
            'key': CAL, 'name': 'Cal',
            'fields': [
                {'key': 'username', 'name': 'User Name', 'type': 'text'},
                {'key': 'email', 'name': 'Email', 'type': 'email'},
                {'key': 'password', 'name': 'Password', 'type': 'password'}
            ],
        },
        {
            'key': MAX, 'name': 'Max',
            'fields': [
                {'key': 'username', 'name': 'User Name', 'type': 'text'},
                {'key': 'password', 'name': 'Password', 'type': 'password'}
            ],
        }
    ]


class TagConstants:
    """Constants for transaction tags."""
    
    MONTHLY_FIXED = 'MONTHLY FIXED'
    PERIODIC = 'PERIODIC'
    CONTINUOUS = 'CONTINUOUS'
    
    TYPE_CHOICES = (
        (MONTHLY_FIXED, "MONTHLY FIXED"),  # חודשיות קבועות
        (PERIODIC, "PERIODIC"),  # תקופתיות
        (CONTINUOUS, "CONTINUOUS"),  # שטפות
    )


class MessageConstants:
    """Constants for chat messages."""
    
    # Sender types
    USER = "user"
    AGENT = "agent"
    
    # Content types
    TEXT = "text"
    IMAGE = "image"
    BUTTONS = "buttons"
    CHART = "chart"
    
    SENDER_CHOICES = [
        (USER, "User"),
        (AGENT, "Agent"),
    ]
    
    CONTENT_TYPE_CHOICES = [
        (TEXT, "Text"),
        (IMAGE, "Image"),
        (BUTTONS, "Buttons"),
        (CHART, "Chart"),
    ]


def validate_credential_json(credential_data: str) -> Dict[str, Any]:
    """
    Validate and parse credential JSON data.
    
    Args:
        credential_data: JSON string containing credential information
        
    Returns:
        Parsed credential dictionary
        
    Raises:
        ValueError: If JSON is invalid
    """
    try:
        if isinstance(credential_data, dict):
            return credential_data
        return json.loads(credential_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid credential JSON: {e}")


def generate_user_code() -> int:
    """
    Generate a random user code between 10000 and 90000.
    
    Returns:
        Random integer user code
    """
    return random.randint(10000, 90000)


def get_company_type(company_name: str) -> str:
    """
    Get the account type for a given company.
    
    Args:
        company_name: Name of the financial company
        
    Returns:
        Account type (BANK or DEBIT_CARD)
        
    Raises:
        ValueError: If company name is not recognized
    """
    if company_name in CompanyConstants.COMPANY_TYPE:
        return CompanyConstants.COMPANY_TYPE[company_name]
    raise ValueError(f"Unknown company: {company_name}")


def validate_tag_type(tag_type: str) -> bool:
    """
    Validate if a tag type is allowed.
    
    Args:
        tag_type: Tag type to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_types = [choice[0] for choice in TagConstants.TYPE_CHOICES]
    return tag_type in valid_types


def validate_message_sender(sender: str) -> bool:
    """
    Validate if a message sender type is allowed.
    
    Args:
        sender: Sender type to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_senders = [choice[0] for choice in MessageConstants.SENDER_CHOICES]
    return sender in valid_senders


def validate_message_content_type(content_type: str) -> bool:
    """
    Validate if a message content type is allowed.
    
    Args:
        content_type: Content type to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_types = [choice[0] for choice in MessageConstants.CONTENT_TYPE_CHOICES]
    return content_type in valid_types


def format_transaction_identifier(name: str, date: str, value: float) -> str:
    """
    Generate a unique identifier for a transaction.
    
    Args:
        name: Transaction name
        date: Transaction date (YYYY-MM-DD format)
        value: Transaction value
        
    Returns:
        Formatted transaction identifier
    """
    # Create base identifier with date and value
    suffix = f"{date}_{abs(value):.2f}"
    # Calculate available space for name
    max_name_length = 64 - len(suffix) - 1  # -1 for underscore
    
    # Truncate name if needed
    clean_name = name.replace(' ', '_')
    if len(clean_name) > max_name_length:
        clean_name = clean_name[:max_name_length]
    
    return f"{clean_name}_{suffix}" 