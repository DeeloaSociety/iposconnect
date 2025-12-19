from unittest import TestCase

from iposconnect.dataframe import IposDataframe


class TestIposDataframe(TestCase):
    def setUp(self):
        self.iposDataframe = IposDataframe()

    def testConstruction(self):
        self.assertIsNotNone(self.iposDataframe)

    def testMasterItem(self):
        self.assertIsNotNone(self.iposDataframe.item())

    def testMasterItemStock(self):
        self.assertIsNotNone(self.iposDataframe.itemStock())

    def tearDown(self):
        self.iposDataframe.connection.disconnect()


if __name__ == '__main__':
    unittest.main()
