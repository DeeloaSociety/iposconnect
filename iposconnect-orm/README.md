## iPos Desktop Connect - ORM

#### API wrapper uses [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

### How to install
To install the package, run the following command:
```shell
git clone https://github.com/DeeloaSociety/iposconnect
cd iposconnect/iposconnect-orm
pip install .
```
Download from git resources:
```shell
pip install git+https://github.com/DeeloaSociety/iposconnect.git@develop#subdirectory=iposconnect-orm
```
set database connection in your .env

### Import libraries
```python
from sqlalchemy import select
from sqlalchemy.orm import Session

from iposconnect.orm import database
from iposconnect.orm import Journal
```

### Fetch data with context processing
```python
with database.get_db_session() as db_session:
    execute_db = db_session.execute(select(Journal)).scalars()
    print(execute_db.first().account_code)
```

### License
MIT