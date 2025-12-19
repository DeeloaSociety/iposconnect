from unittest import TestCase

from sqlalchemy import select
from sqlalchemy.orm import Session

from iposconnect.orm import database
from iposconnect.orm import (
    Currency
)


class TestSession(TestCase):
    def setUp(self):
        self.db: Session = next(database.get_db())

    def test_execute_of_user(self):
        self.assertIsNotNone(self.db.execute(select(Currency)))

    def test_execute_with_context(self):
        with database.get_db_session() as db_session:
            db_execute = db_session.query(Currency)
            assert db_execute.first() is not None


if __name__ == '__main__':
    unittest.main()
