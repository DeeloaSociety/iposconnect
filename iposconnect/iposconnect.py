import os
from dotenv import load_dotenv
import ibis

from .master import Item, ItemStock
from .account import Account, Journal, JournalV5
from .transactions import (
    SalesInvoice, SalesInvoiceDetails,
    PurchaseReceipt, PurchaseReceiptDetails,
)

load_dotenv()


class IposConnect:
    def __init__(
            self,
            host=os.getenv("IBIS_POSTGRES_HOST"),
            port=os.getenv("IBIS_POSTGRES_PORT"),
            user=os.getenv("IBIS_POSTGRES_USER"),
            password=os.getenv("IBIS_POSTGRES_PASSWORD"),
            database=os.getenv("IBIS_POSTGRES_DATABASE"),
    ):
        self.connection = ibis.connect(f"postgres://{user}:{password}@{host}:{port}/{database}")

    def item(self):
        return Item(self.connection)

    def itemStock(self):
        return ItemStock(self.connection)

    def account(self):
        return Account(self.connection)

    def journal(self):
        return Journal(self.connection)

    def journalV5(self):
        return JournalV5(self.connection)

    def salesInvoice(self):
        return SalesInvoice(self.connection)

    def salesInvoiceDetails(self):
        return SalesInvoiceDetails(self.connection)

    def purchaseReceipt(self):
        return PurchaseReceipt(self.connection)

    def purchaseReceiptDetails(self):
        return PurchaseReceiptDetails(self.connection)
