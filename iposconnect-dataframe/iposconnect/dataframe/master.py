from ibis import Table

from .base import BaseTable, BaseBuilder


class Item(BaseTable):
    def extract(self) -> Table:
        self.table = self._backend.table("tbl_item")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    kode_item="kodeitem",
                    nama_item="namaitem",
                    stock_minimal="stokmin",
                    harga_pokok="hargapokok",
                    harga_jual="hargajual1",
                )
            )
        )

        self.table = (
            self.table.mutate(
                stock_minimal=self.table.stock_minimal.cast("decimal"),
                harga_pokok=self.table.harga_pokok.cast("decimal(19, 2)"),
                harga_jual=self.table.harga_jual.cast("decimal(19, 2)"),
            )
        )

        return self.table

    def load(self) -> Table:
        return self.transform()

    def parts(self):
        return Item.ItemBuilder(self.load())

    class ItemBuilder(BaseBuilder):
        def byItemCode(self, item_code: str):
            self.table = self.table.filter(
                self.table.kode_item == item_code
            )
            return self


class ItemStock(BaseTable):
    def extract(self) -> Table:
        self.table = self._backend.table("tbl_itemstok")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    kode_item="kodeitem",
                )
            )
        )

        self.table = (
           self.table.mutate(
               stok=self.table.stok.cast("decimal"),
           )
        )

        return self.table

    def load(self) -> Table:
        return self.transform()

    def parts(self):
        return ItemStock.ItemStockBuilder(self.load())

    class ItemStockBuilder(BaseBuilder):
        def agg(self, group_by: list[str]) -> Table:
            return (
                self.table.group_by(group_by)
                .aggregate(
                    stok=self.table.stok.sum(),
                )
            )

        def byItemCode(self, item_code: str):
            self.table = self.agg(["kode_item"]).filter(
                self.table.kode_item == item_code
            )
            return self
