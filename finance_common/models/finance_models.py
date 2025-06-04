import datetime
import json
import random

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship

from ..db import Base


class DateInput(Base):
    __tablename__ = "date_input"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    name = Column(String(128))
    date = Column(Date)


class Credential(Base):
    __tablename__ = "credential"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    company = Column(String(30))
    credential = Column(String(512))
    last_scanned = Column(Date)
    type = Column(String(32))
    additional_info = Column(JSON, default=dict)


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    key = Column(String(128))
    name = Column(String(128))
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    expense = Column(Boolean, default=False)
    type = Column(String(32))


class TagGoal(Base):
    __tablename__ = "tag_goal"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))
    value = Column(Float)


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    credential_id = Column(Integer, ForeignKey("credential.id"))
    date = Column(Date)
    name = Column(String(200))
    value = Column(Float)
    month = Column(Integer)
    tag_id = Column(Integer, ForeignKey("tag.id"))
    month_date = Column(Date)
    bank = Column(Boolean, default=False)
    identifier = Column(String(64))


class RecurringTransaction(Base):
    __tablename__ = "recurring_transaction"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    name = Column(String(200))
    date = Column(Date)
    credential_id = Column(Integer, ForeignKey("credential.id"))
    value = Column(Float)


class TransactionNameTag(Base):
    __tablename__ = "transaction_name_tag"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    transaction_name = Column(String(200))
    tag_id = Column(Integer, ForeignKey("tag.id"))


class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))
    date = Column(Date)
    value = Column(Float)


class AdditionalInfo(Base):
    __tablename__ = "additional_info"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(JSON, default=dict)

    @classmethod
    def create_user_code(cls, session):
        code = random.randint(10000, 90000)
        while session.query(cls).filter(cls.value['user_code'].as_integer() == code).count() > 0:
            code = random.randint(10000, 90000)
        return code


class DiscountCredential(Base):
    __tablename__ = "discount_credential"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    password = Column(String(255))
    user_identification = Column(String(255))
    user_name = Column(String(255))


class ErrorLog(Base):
    __tablename__ = "error_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    message = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

