# finance_common

Shared SQLAlchemy models and database utilities used across services.

This package defines the database connection via `finance_common.db` and now
contains SQLAlchemy equivalents of the core Django models (accounts,
credentials, transactions, conversations, etc.). Each microservice can import
these models along with the `SessionLocal` session factory to query the database
without loading the Django ORM.
