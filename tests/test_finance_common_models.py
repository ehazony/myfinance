import importlib
import os


def setup_module(module):
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    import finance_common.db
    importlib.reload(finance_common.db)


def test_create_account():
    from finance_common import SessionLocal, Base, Account

    Base.metadata.create_all(bind=finance_common.db.engine)
    with SessionLocal() as session:
        acc = Account(name="demo")
        session.add(acc)
        session.commit()
        assert acc.id is not None
