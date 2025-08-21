from ibis import Table, ifelse
from pandas import DataFrame

from .base import BaseTable, BaseBuilder, BaseForcast
from .master import Item


class Invoice(BaseTable):
    def extract(self) -> Table:
        self.table = self._backend.table("tbl_ikhd")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    invoice_created="tanggal",
                    invoice_id="notransaksi",
                    order_id="notrsorder",
                    return_id="notrsretur",
                    user="user1",
                    kode_penjual="kodesales",
                    jumlah_item="totalitem",
                    sub_total="subtotal",
                    potongan_invoice="potfaktur",
                    biaya_lain="biayalain",
                    total_akhir="totalakhir",
                    jumlah_emoney="jmlemoney",
                    produk_emoney="byr_emoney_prod",
                    jumlah_bayar_tunai="jmltunai",
                    jumlah_bayar_kredit="jmlkredit",
                    jumlah_bayar_kartu_debit="jmldebit",
                    jumlah_bayar_kartu_kredit="jmlkk",
                )
            )
        )

        self.table = (
            self.table.mutate(
                invoice_created=self.table.invoice_created.cast("date"),
                jumlah_item=self.table.jumlah_item.cast("decimal"),
                sub_total=self.table.sub_total.cast("decimal(19, 2)"),
                potongan_invoice=self.table.potongan_invoice.cast("decimal(19, 2)"),
                biaya_lain=self.table.biaya_lain.cast("decimal(19, 2)"),
                total_akhir=self.table.total_akhir.cast("decimal(19, 2)"),
                jumlah_emoney=self.table.jumlah_emoney.cast("decimal(19, 2)"),
                jumlah_bayar_tunai=self.table.jumlah_bayar_tunai.cast("decimal(19, 2)"),
                jumlah_bayar_kredit=self.table.jumlah_bayar_kredit.cast("decimal(19, 2)"),
                jumlah_bayar_kartu_debit=self.table.jumlah_bayar_kartu_debit.cast("decimal(19, 2)"),
                jumlah_bayar_kartu_kredit=self.table.jumlah_bayar_kartu_kredit.cast("decimal(19, 2)"),
            )
        )

        self.table = (
            self.table.mutate(
                jumlah_bayar_tunai=ifelse(
                    self.table.jumlah_bayar_tunai >= self.table.total_akhir,
                    self.table.total_akhir, self.table.jumlah_bayar_tunai
                ),
            )
        )

        self.table = (
            self.table.order_by("invoice_created")
        )

        return self.table

    def load(self) -> Table:
        self.table = self.transform()

        if self._is_between:
            self.table = self.table.filter(
                self.table.invoice_created.between(self._start_date, self._end_date)
            )

        return self.table


class SalesInvoice(BaseTable):
    def extract(self):
        invoice = Invoice(self._backend)
        _invoice = invoice.load()

        self.table = _invoice.filter(
            _invoice.tipe.isin(["JL", "KSR"])
        )

        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    lokasi_keluar="kantordari",
                    kode_pelanggan="kodesupel",
                )
            )
        )

        return self.table

    def load(self) -> Table:
        self.table = self.transform()

        if self._is_between:
            self.table = self.table.filter(
                self.table.invoice_created.between(self._start_date, self._end_date)
            )

        return self.table

    def parts(self):
        return SalesInvoice.SalesInvoiceBuilder(self.load())

    class SalesInvoiceBuilder(BaseBuilder):
        def recap(self) -> Table:
            return self.table.select("invoice_id", "invoice_created",
                                     "lokasi_keluar", "kode_pelanggan", "jumlah_item", "sub_total",
                                     "potongan_invoice", "pajak", "biaya_lain",
                                     "total_akhir", "jumlah_bayar_tunai",
                                     "jumlah_bayar_kredit", "jumlah_emoney", "produk_emoney")

        def recap2(self) -> Table:
            return self.table.select("invoice_id", "invoice_created",
                                     "lokasi_keluar", "kode_pelanggan", "jumlah_item", "sub_total",
                                     "potongan_invoice", "pajak", "biaya_lain",
                                     "total_akhir")

        def totalRecap(self) -> Table:
            return (
                self.table.aggregate(
                    jumlah_item=self.table.jumlah_item.sum(),
                    sub_total=self.table.sub_total.sum(),
                    potongan_invoice=self.table.potongan_invoice.sum(),
                    pajak=self.table.pajak.sum(),
                    biaya_lain=self.table.biaya_lain.sum(),
                    total_akhir=self.table.total_akhir.sum(),
                    jumlah_bayar_tunai=self.table.jumlah_bayar_tunai.sum(),
                    jumlah_bayar_kredit=self.table.jumlah_bayar_kredit.sum(),
                )
            )

        def agg(self, group_by: list[str]) -> Table:
            return (
                self.table.group_by(group_by)
                .aggregate(
                    jumlah_transaksi=self.table.invoice_id.count(),
                    total_transaksi=self.table.total_akhir.sum(),
                    jumlah_bayar_tunai=self.table.jumlah_bayar_tunai.sum(),
                    jumlah_bayar_kredit=self.table.jumlah_bayar_kredit.sum(),
                    jumlah_bayar_kartu_debit=self.table.jumlah_bayar_kartu_debit.sum(),
                    jumlah_bayar_kartu_kredit=self.table.jumlah_bayar_kartu_kredit.sum(),
                )
            )

        def byDaily(self) -> Table:
            return self.agg(["invoice_created"])

        def byCustomer(self) -> Table:
            return self.agg(["kode_pelanggan"])

        def bySeller(self) -> Table:
            return self.agg(["kode_penjual", "kode_pelanggan"])


class InvoiceDetails(BaseTable):
    def extract(self) -> Table:
        self.table = self._backend.table("tbl_ikdt")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    invoice_detail_id="iddetail",
                    invoice_id="notransaksi",
                    kode_item="kodeitem",
                    jumlah_pesanan="jmlpesan",
                    potongan_item="potongan",
                )
            )
        )

        self.table = (
            self.table.mutate(
                jumlah=self.table.jumlah.cast("decimal"),
                jumlah_pesanan=self.table.jumlah_pesanan.cast("decimal"),
                harga=self.table.harga.cast("decimal(19, 2)"),
                potongan_item=self.table.potongan_item.cast("decimal(19, 2)"),
            )
        )

        return self.table

    def load(self) -> Table:
        return self.transform()


class SalesInvoiceDetails(BaseTable):
    def extract(self) -> Table:
        item = Item(self._backend)
        salesInvoice = SalesInvoice(self._backend)
        invoiceDetails = InvoiceDetails(self._backend)

        _item = item.load()
        _salesInvoice = salesInvoice.load()
        _invoiceDetails = invoiceDetails.load()

        self.table = (
            _invoiceDetails.join(
                _salesInvoice, [_invoiceDetails.invoice_id == _salesInvoice.invoice_id]
            ).join(
                _item, [_invoiceDetails.kode_item == _item.kode_item]
            )
        )

        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.select("invoice_id", "invoice_created", "tipe", "lokasi_keluar",
                              "user", "kode_pelanggan", "kode_penjual", "kode_item",
                              "nama_item", "merek", "jenis", "jumlah", "satuan",
                              "harga", "potongan_item", "total")
        )

        return self.table

    def load(self) -> Table:
        self.table = self.transform()

        if self._is_between:
            self.table = self.table.filter(
                self.table.invoice_created.between(self._start_date, self._end_date)
            )

        return self.table

    def parts(self):
        return SalesInvoiceDetails.SalesInvoiceDetailsBuilder(self.load())

    class SalesInvoiceDetailsBuilder(BaseBuilder):
        def byItemCode(self, item_code):
            self.table = (
                self.table.filter(self.table.kode_item == item_code)
            )
            return self

        def agg(self, group_by: list[str]) -> Table:
            return (
                self.table.group_by(group_by)
                .aggregate(
                    jumlah_item=self.table.jumlah.sum(),
                    total_harga=self.table.total.sum(),
                )
            )

        def byDaily(self) -> Table:
            return self.agg(["invoice_created", "kode_item", "nama_item", "jenis", "merek"])

        def byCustomer(self) -> Table:
            return self.agg(["kode_item", "nama_item", "jenis", "merek", "kode_pelanggan"])

        def bySeller(self) -> Table:
            return (
                self.agg(["kode_item", "nama_item", "jenis", "merek", "kode_penjual"])
                .filter(self.table.kode_penjual.notnull())
            )

        def revenueAgg(self, select: list[str]) -> Table:
            revenue = self.agg(select)

            return (
                revenue.mutate(
                    total_pendapatan=revenue.total_harga,
                    rasio_pendapatan=(revenue.total_harga / revenue.total_harga.sum().as_scalar()) * 100
                )
            )

        def revenueByItemCode(self) -> Table:
            return self.revenueAgg(["kode_item"])

        def revenueByItemUnit(self) -> Table:
            return self.revenueAgg(["satuan"])

        def revenueByItemCategory(self) -> Table:
            return self.revenueAgg(["jenis"])

        def revenueByItemBrand(self) -> Table:
            return self.revenueAgg(["merek"])

        def revenueByItemPrice(self) -> Table:
            return self.revenueAgg(["harga"])

        def revenueByCustomer(self) -> Table:
            return self.revenueAgg(["kode_pelanggan"])

        def revenueBySeller(self) -> Table:
            return self.revenueAgg(["kode_penjual"])

        def revenueByType(self) -> Table:
            return self.revenueAgg(["tipe"])

        def revenueByWarehouse(self) -> Table:
            return self.revenueAgg(["lokasi_keluar"])

    def forcast(self, item_kode):
        self.table = self.load().filter(
            self.table.kode_item == item_kode,
        )

        df = (
            self.table.group_by("invoice_created", "kode_item", "nama_item")
            .aggregate(
                jumlah_item=self.table.jumlah.sum(),
            )
        )

        return SalesInvoiceDetails.SalesForcast(df=df.to_pandas())

    class SalesForcast(BaseForcast):
        def extract(self) -> DataFrame:
            self.df = self.df.astype({
                "invoice_created": "datetime64[ns]",
                "kode_item": "category",
                "jumlah_item": "int32"
            })
            return self.df

        def transform(self):
            import pandas as pd
            self.df = self.extract()

            date_index = pd.DatetimeIndex(self.df.invoice_created)
            df_with_index = self.df.set_index(date_index)

            start_date = date_index.min()
            end_date = date_index.max()

            # set specify datetime with frequency
            complete_date_range = pd.date_range(start=start_date, end=end_date, freq='D')

            if self.df.index.size != complete_date_range.values.size:
                # reindexing
                self.df = df_with_index.reindex(complete_date_range)

            # cleaning the column
            if len(self.df.invoice_created) > 0:
                self.df = self.df.drop(columns=["invoice_created"])

            # fill the rows
            self.df = self.df.fillna(
                {
                    'kode_item': self.df["kode_item"].bfill(),
                    'nama_item': self.df["nama_item"].bfill(),
                    'jumlah_item': 0.0}
            )

            return self.df

        def fit(self):
            # Modelling and Forecasting
            from lightgbm import LGBMRegressor
            from skforecast.recursive import ForecasterRecursive

            # create forecaster
            self._forecaster = ForecasterRecursive(
                regressor=LGBMRegressor(random_state=int(self.df.kode_item.size / 2), verbose=-1),
                lags=(self.df.kode_item.size - 1)
            )

            # fitting
            self._forecaster.fit(y=self._target)
            return self


class Receipt(BaseTable):
    def extract(self) -> Table:
        self.table = self._backend.table("tbl_imhd")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    receipt_created="tanggal",
                    receipt_id="notransaksi",
                    order_id="notrsorder",
                    return_id="notrsretur",
                    user="user1",
                    jumlah_item="totalitem",
                    sub_total="subtotal",
                    potongan_receipt="potfaktur",
                    biaya_lain="biayalain",
                    total_akhir="totalakhir",
                    jumlah_bayar_tunai="jmltunai",
                    jumlah_bayar_kredit="jmlkredit",
                )
            )
        )

        self.table = (
            self.table.mutate(
                receipt_created=self.table.receipt_created.cast("date"),
                jumlah_item=self.table.jumlah_item.cast("decimal"),
                sub_total=self.table.sub_total.cast("decimal(19, 2)"),
                potongan_receipt=self.table.potongan_receipt.cast("decimal(19, 2)"),
                biaya_lain=self.table.biaya_lain.cast("decimal(19, 2)"),
                total_akhir=self.table.total_akhir.cast("decimal(19, 2)"),
                jumlah_bayar_tunai=self.table.jumlah_bayar_tunai.cast("decimal(19, 2)"),
                jumlah_bayar_kredit=self.table.jumlah_bayar_kredit.cast("decimal(19, 2)"),
            )
        )

        self.table = (
            self.table.order_by("receipt_created")
        )

        return self.table

    def load(self) -> Table:
        self.table = self.transform()

        if self._is_between:
            self.table = self.table.filter(
                self.table.receipt_created.between(self._start_date, self._end_date)
            )

        return self.table


class PurchaseReceipt(BaseTable):
    def extract(self):
        receipt = Receipt(self._backend)

        self.table = receipt.load().filter(
            receipt.load().tipe.isin(["BL"])
        )

        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    lokasi_masuk="kantortujuan",
                    kode_pemasok="kodesupel",
                )
            )
        )

        return self.table

    def load(self) -> Table:
        self.table = self.transform()

        if self._is_between:
            self.table = self.table.filter(
                self.table.receipt_created.between(self._start_date, self._end_date)
            )

        return self.table

    def parts(self):
        return PurchaseReceipt.PurchaseReceiptBuilder(self.load())

    class PurchaseReceiptBuilder(BaseBuilder):
        def recap(self) -> Table:
            return self.table.select("receipt_id", "receipt_created", "lokasi_masuk",
                                     "kode_pemasok", "jumlah_item", "sub_total",
                                     "potongan_receipt", "pajak", "biaya_lain", "total_akhir",
                                     "jumlah_bayar_tunai", "jumlah_bayar_kredit")

        def recap2(self) -> Table:
            return self.table.select("receipt_id", "receipt_created",
                                     "lokasi_masuk", "kode_pemasok", "jumlah_item", "sub_total",
                                     "potongan_receipt", "pajak", "biaya_lain", "total_akhir")

        def totalRecap(self) -> Table:
            return (
                self.table.aggregate(
                    jumlah_item=self.table.jumlah_item.sum(),
                    sub_total=self.table.sub_total.sum(),
                    potongan_receipt=self.table.potongan_receipt.sum(),
                    pajak=self.table.pajak.sum(),
                    biaya_lain=self.table.biaya_lain.sum(),
                    total_akhir=self.table.total_akhir.sum(),
                    jumlah_bayar_tunai=self.table.jumlah_bayar_tunai.sum(),
                    jumlah_bayar_kredit=self.table.jumlah_bayar_kredit.sum(),
                )
            )

        def agg(self, group_by: list[str]) -> Table:
            return (
                self.table.group_by(group_by)
                .aggregate(
                    jumlah_transaksi=self.table.receipt_id.count(),
                    total_transaksi=self.table.total_akhir.sum(),
                    jumlah_bayar_tunai=self.table.jumlah_bayar_tunai.sum(),
                    jumlah_bayar_kredit=self.table.jumlah_bayar_kredit.sum(),
                )
            )

        def byDaily(self) -> Table:
            return self.agg(["receipt_created"])

        def bySupplier(self) -> Table:
            return self.agg(["kode_pemasok"])


class ReceiptDetails(BaseTable):
    def extract(self) -> Table:
        self.table = self._backend.table("tbl_imdt")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    receipt_detail_id="iddetail",
                    receipt_id="notransaksi",
                    kode_item="kodeitem",
                    jumlah_pesanan="jmlpesan",
                    potongan_item="potongan",
                )
            )
        )

        self.table = (
            self.table.mutate(
                jumlah=self.table.jumlah.cast("decimal"),
                jumlah_pesanan=self.table.jumlah_pesanan.cast("decimal"),
                harga=self.table.harga.cast("decimal(19, 2)"),
                potongan_item=self.table.potongan_item.cast("decimal(19, 2)"),
            )
        )

        return self.table

    def load(self) -> Table:
        return self.transform()


class PurchaseReceiptDetails(BaseTable):
    def extract(self) -> Table:
        item = Item(self._backend)
        purchaseReceipt = PurchaseReceipt(self._backend)
        receiptDetails = ReceiptDetails(self._backend)

        _item = item.load()
        _purchaseReceipt = purchaseReceipt.load()
        _receiptDetails = receiptDetails.load()

        self.table = (
            _receiptDetails.join(
                _purchaseReceipt, [_receiptDetails.receipt_id == _purchaseReceipt.receipt_id]
            ).join(
                _item, [_receiptDetails.kode_item == _item.kode_item]
            )
        )

        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.select("receipt_id", "receipt_created", "tipe", "lokasi_masuk",
                              "user", "kode_pemasok", "kode_item", "nama_item", "merek",
                              "jenis", "jumlah", "satuan", "harga", "potongan_item", "total")
        )

        return self.table

    def load(self) -> Table:
        self.table = self.transform()

        if self._is_between:
            self.table = self.table.filter(
                self.table.receipt_created.between(self._start_date, self._end_date)
            )

        return self.table

    def parts(self):
        return PurchaseReceiptDetails.PurchaseReceiptDetailsBuilder(self.load())

    class PurchaseReceiptDetailsBuilder(BaseBuilder):
        def byItemCode(self, item_code):
            self.table = (
                self.table.filter(self.table.kode_item == item_code)
            )
            return self

        def agg(self, group_by: list[str]) -> Table:
            return (
                self.table.group_by(group_by)
                .aggregate(
                    jumlah_item=self.table.jumlah.sum(),
                    total_harga=self.table.total.sum(),
                )
            )

        def byDaily(self) -> Table:
            return self.agg(["receipt_created", "kode_item", "nama_item", "jenis", "merek"])

        def byCustomer(self) -> Table:
            return (
                self.agg(["kode_item", "nama_item", "jenis", "merek", "kode_pemasok", "lokasi_masuk"])
                .filter(self.table.kode_pemasok.notnull())
            )

        def receiptAgg(self, select: list[str]) -> Table:
            receipt = self.agg(select)

            return (
                receipt.mutate(
                    total_penerimaan=receipt.total_harga,
                    rasio_penerimaan=(receipt.total_harga / receipt.total_harga.sum().as_scalar()) * 100
                )
            )

        def receiptByItemCode(self) -> Table:
            return self.receiptAgg(["kode_item", "lokasi_masuk", "kode_pemasok"])

        def receiptBySupplier(self) -> Table:
            return self.receiptAgg(["kode_pemasok"])

        def receiptByWarehouse(self) -> Table:
            return self.receiptAgg(["lokasi_masuk"])
