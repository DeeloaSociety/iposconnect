from unittest import TestCase

from iposconnect import IposConnect


class TestIposConnect(TestCase):
    def setUp(self):
        self.iposConnect = IposConnect()

    def testConstruction(self):
        self.assertIsNotNone(self.iposConnect)

    def testMasterItem(self):
        self.assertIsNotNone(self.iposConnect.item())

    def testMasterItemStock(self):
        self.assertIsNotNone(self.iposConnect.itemStock())

    def tearDown(self):
        self.iposConnect.connection.disconnect()
