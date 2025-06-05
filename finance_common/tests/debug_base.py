from finance_common.db import Base
import finance_common.models.account

print('Base id:', id(Base))
print('Registered tables:', Base.metadata.tables.keys()) 