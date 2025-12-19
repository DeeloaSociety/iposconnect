from decimal import Decimal
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, DateTime, String, Integer, DECIMAL, TEXT, BOOLEAN
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class BaseModel(DeclarativeBase):
    __abstract__ = True


class Office(BaseModel):
    """Office model for storing Offices information"""

    __tablename__ = "tbl_kantor"

    office_code: Mapped[str] = mapped_column("kodekantor", String(50), primary_key=True, nullable=False)
    purpose: Mapped[str] = mapped_column("fungsi", String(20))
    office_name: Mapped[str] = mapped_column("namakantor", String(200))
    address: Mapped[str] = mapped_column("alamat", TEXT)
    phone: Mapped[str] = mapped_column(String("notelepon", 150))
    fax: Mapped[str] = mapped_column(String(150))
    branch: Mapped[bool] = mapped_column("cabang", BOOLEAN, default=False)
    account_code: Mapped[str] = mapped_column("kodeacc", String(30))
    whatsapp: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    tax_type: Mapped[str] = mapped_column("jenis_pajak", String(10))
    journal: Mapped[List["Journal"]] = relationship(back_populates="office")
    item: Mapped[List["Item"]] = relationship(back_populates="office")
    item_stock: Mapped[List["ItemStok"]] = relationship(back_populates="office")
    item_opname: Mapped[List["ItemOpname"]] = relationship(back_populates="office")
    inventory_in: Mapped[List["InventoryIn"]] = relationship(back_populates="office")
    inventory_out: Mapped[List["InventoryOut"]] = relationship(back_populates="office")


class Currency(BaseModel):
    """Currency model for storing Currencies information"""

    __tablename__ = "tbl_matauang"

    currency: Mapped[str] = mapped_column("matauang", String(50), primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column("ketmatauang", String(100))
    rate: Mapped[Decimal] = mapped_column(DECIMAL(35, 20), default=0)
    default: Mapped[bool] = mapped_column("utama", BOOLEAN, default=False)
    account_payable: Mapped[str] = mapped_column("acc_hutang", String(50))
    account_receivable: Mapped[str] = mapped_column("acc_piutang", String(50))
    account_cash: Mapped[str] = mapped_column("acc_byrtunai", String(50))
    account_bank: Mapped[str] = mapped_column("acc_byrbank", String(50))
    type: Mapped[str] = mapped_column("tipe", String(5))
    chart_of_account: Mapped[List["ChartOfAccount"]] = relationship(back_populates="currency")
    journal: Mapped[List["Journal"]] = relationship(back_populates="currency")
    item: Mapped[List["Item"]] = relationship(back_populates="currency")
    inventory_in: Mapped[List["InventoryIn"]] = relationship(back_populates="currency")


class ChartOfAccount(BaseModel):
    """Chart of Account model for storing Chart of accounts information"""

    __tablename__ = "tbl_perkiraan"

    account_code: Mapped[str] = mapped_column("kodeacc", String(30), primary_key=True, nullable=False)
    account_parent: Mapped[str] = mapped_column("parentacc", String(30), nullable=True)
    group: Mapped[str] = mapped_column("kelompok", String(2))
    type: Mapped[str] = mapped_column("tipe", String(2))
    account_name: Mapped[str] = mapped_column("namaacc", String(200))
    currency_name: Mapped[str] = mapped_column("matauang", String(50), ForeignKey("tbl_matauang.matauang"))
    activity: Mapped[str] = mapped_column("aktivitas", String(15), default="Operasional")
    date_updated: Mapped[datetime] = mapped_column("dateupd", DateTime, server_default=func.now(), onupdate=func.now())
    currency: Mapped["Currency"] = relationship(back_populates="chart_of_account")
    journal: Mapped[List["Journal"]] = relationship(back_populates="chart_of_account")
    item_opname: Mapped[List["ItemOpname"]] = relationship(back_populates="chart_of_account")


class CategoryOfAccount(BaseModel):
    """Category of Account model for storing Categories of Accounts information"""

    __tablename__ = "tbl_kategori_kas"

    category_code: Mapped[str] = mapped_column("kodekategori", String(20), primary_key=True, nullable=False)
    category_name: Mapped[str] = mapped_column("namakategori", String(150))
    group: Mapped[str] = mapped_column("grupaktivitas", String(20))
    flagdel: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    journal: Mapped[List["Journal"]] = relationship(back_populates="category_of_account")


class Journal(BaseModel):
    """Journal model for storing Journals information"""

    __tablename__ = "tbl_accjurnal"

    detail_id: Mapped[str] = mapped_column("iddetail", String(150), primary_key=True, nullable=False)
    no_transaction: Mapped[str] = mapped_column("notransaksi", String(150), index=True)
    sequence: Mapped[int] = mapped_column("nourut", Integer)
    input_type: Mapped[str] = mapped_column("tipeinput", String(5))
    account_code: Mapped[str] = mapped_column("kodeacc", String(30), ForeignKey("tbl_perkiraan.kodeacc"))
    kind: Mapped[str] = mapped_column("jenis", String(20))
    description: Mapped[str] = mapped_column("keterangan", TEXT)
    currency_name: Mapped[str] = mapped_column("matauang", String(50), ForeignKey("tbl_matauang.matauang"))
    rate: Mapped[Decimal] = mapped_column(DECIMAL(35, 20), default=0)
    amount: Mapped[Decimal] = mapped_column("jumlah", DECIMAL(35, 20), default=0)
    position: Mapped[str] = mapped_column("posisi", String(5))
    debit: Mapped[Decimal] = mapped_column("debet", DECIMAL(35, 20), default=0)
    credit: Mapped[Decimal] = mapped_column("kredit", DECIMAL(35, 20), default=0)
    office_code: Mapped[str] = mapped_column("kantor", String(50), ForeignKey("tbl_kantor.kodekantor"))
    module: Mapped[str] = mapped_column("modul", String(20))
    category_code: Mapped[str] = mapped_column("kategori_kas", String(20), ForeignKey("tbl_kategori_kas.kodekategori"))
    cash_of_bank: Mapped[bool] = mapped_column("kasbank", BOOLEAN)
    date: Mapped[datetime] = mapped_column("tanggal", DateTime, server_default=func.now(), onupdate=func.now())
    chart_of_account: Mapped["ChartOfAccount"] = relationship(back_populates="journal")
    currency: Mapped["Currency"] = relationship(back_populates="journal")
    office: Mapped["Office"] = relationship(back_populates="journal")
    category_of_account: Mapped["CategoryOfAccount"] = relationship(back_populates="journal")


class Item(BaseModel):
    """Item model for storing Items information"""

    __tablename__ = "tbl_item"

    item_code: Mapped[str] = mapped_column("kodeitem", String(100), primary_key=True, unique=True, nullable=False)
    item_name: Mapped[str] = mapped_column("namaitem", TEXT)
    kind: Mapped[str] = mapped_column("jenis", String(50))
    type: Mapped[str] = mapped_column("tipe", String(15), default="Y")
    currency_name: Mapped[str] = mapped_column("matauang", String(50), ForeignKey("tbl_matauang.matauang"))
    serial: Mapped[str] = mapped_column(String(15), default="N")
    consignment: Mapped[str] = mapped_column("konsinyasi", String(15), default="N")
    minimum_stock: Mapped[Decimal] = mapped_column("stokmin", DECIMAL(20, 3), default=0)
    bin: Mapped[str] = mapped_column("rak", String(100))
    unit: Mapped[str] = mapped_column("satuan", String(50))
    cogs: Mapped[Decimal] = mapped_column("hargapokok", DECIMAL(35, 20), default=0)
    percent_of_sell_price: Mapped[Decimal] = mapped_column("prhargajual1", DECIMAL(20, 3), default=0)
    sell_price: Mapped[Decimal] = mapped_column("hargajual1", DECIMAL(20, 3), default=0)
    sell_status: Mapped[str] = mapped_column("statusjual", String(15))
    brand: Mapped[str] = mapped_column("merek", String(50))
    raft_price: Mapped[Decimal] = mapped_column("hargarakit", DECIMAL(20, 3), default=0)
    department: Mapped[str] = mapped_column("dept", String(50), ForeignKey("tbl_kantor.kodekantor"))
    account_cogs: Mapped[str] = mapped_column("acc_hpp", String(30))
    account_income: Mapped[str] = mapped_column("acc_pendapatan", String(30))
    account_inventory: Mapped[str] = mapped_column("acc_persediaan", String(30))
    account_service: Mapped[str] = mapped_column("acc_jasa", String(30))
    account_noninventory: Mapped[str] = mapped_column("acc_noninventory", String(30))
    account_raw_material: Mapped[str] = mapped_column("acc_perbahanbaku", String(30))
    account_workman: Mapped[str] = mapped_column("acc_bytenagakerja", String(30))
    account_overhead: Mapped[str] = mapped_column("acc_byoverhead", String(30))
    date_updated: Mapped[datetime] = mapped_column("dateupd", DateTime, server_default=func.now(), onupdate=func.now())
    image_file: Mapped[str] = mapped_column("gambarfiles", TEXT)
    assembly_price_options: Mapped[bool] = mapped_column("opsihargarakitan", BOOLEAN, default=False)
    currency: Mapped["Currency"] = relationship(back_populates="item")
    office: Mapped["Office"] = relationship(back_populates="item")
    item_opname: Mapped[List["ItemOpname"]] = relationship(back_populates="item")
    inventory_in: Mapped[List["InventoryIn"]] = relationship(back_populates="item")
    inventory_out: Mapped[List["InventoryOut"]] = relationship(back_populates="item")


class ItemStok(BaseModel):
    """Item Stock model for storing Stock of Items information"""

    __tablename__ = "tbl_itemstok"

    item_code: Mapped[str] = mapped_column("kodeitem", String(100), primary_key=True)
    office_code: Mapped[str] = mapped_column("kantor", String(100), ForeignKey("tbl_kantor.kodekantor"))
    stock: Mapped[Decimal] = mapped_column("stok", DECIMAL(20, 3))
    cogs: Mapped[Decimal] = mapped_column("hppdasar", DECIMAL(35, 20), default=0)
    office: Mapped["Office"] = relationship(back_populates="item_stock")


class ItemOpname(BaseModel):
    """Item Opname model for storing Reconciliation of Stock information"""

    __tablename__ = "tbl_itemopname"

    detail_id: Mapped[str] = mapped_column("iddetail", String(150), primary_key=True, unique=True, nullable=False)
    period: Mapped[str] = mapped_column("periode", String(20))
    date: Mapped[datetime] = mapped_column("tanggal", DateTime, server_default=func.now(), onupdate=func.now())
    item_code: Mapped[str] = mapped_column("kodeitem", String(100), ForeignKey("tbl_item.kodeitem"))
    office_code: Mapped[str] = mapped_column("kodekantor", String(50), ForeignKey("tbl_kantor.kodekantor"))
    unit: Mapped[str] = mapped_column("satuan", String(50))
    previous_amount: Mapped[Decimal] = mapped_column("jmlsebelum", DECIMAL(20, 3), default=0)
    physical_quantity: Mapped[Decimal] = mapped_column("jmlfisik", DECIMAL(20, 3), default=0)
    amount_of_difference: Mapped[Decimal] = mapped_column("jmlselisih", DECIMAL(20, 3), default=0)
    account_code: Mapped[str] = mapped_column("kodeacc", String(30), ForeignKey("tbl_perkiraan.kodeacc"))
    user_1: Mapped[str] = mapped_column("user1", String(50))
    date_updated: Mapped[datetime] = mapped_column("dateupd", DateTime, server_default=func.now(), onupdate=func.now())
    price: Mapped[Decimal] = mapped_column("harga", DECIMAL(35, 30), default=0)
    total: Mapped[Decimal] = mapped_column(DECIMAL(20, 3), default=0)
    computer_name: Mapped[str] = mapped_column("compname", String(255))
    number_of_conversions: Mapped[Decimal] = mapped_column("jmlkonversi", DECIMAL(20, 3), default=0)
    description: Mapped[str] = mapped_column("keterangan", TEXT)
    item: Mapped["Item"] = relationship(back_populates="item_opname")
    office: Mapped["Office"] = relationship(back_populates="item_opname")
    chart_of_account: Mapped["ChartOfAccount"] = relationship(back_populates="item_opname")


class InventoryIn(BaseModel):
    """Inventory In model for storing Incoming of Inventories information"""

    __tablename__ = "tbl_item_im"

    detail_id: Mapped[str] = mapped_column("iddetail", String(150), primary_key=True, nullable=False)
    detail_trs_id: Mapped[str] = mapped_column("iddetailtrs", String(150))
    no_transaction: Mapped[str] = mapped_column("notransaksi", String(100))
    office_code: Mapped[str] = mapped_column("kodekantor", String(50), ForeignKey("tbl_kantor.kodekantor"))
    date: Mapped[datetime] = mapped_column("tanggal", DateTime, server_default=func.now(), onupdate=func.now())
    type: Mapped[str] = mapped_column("tipe", String(20))
    currency_name: Mapped[str] = mapped_column("matauang", String(50), ForeignKey("tbl_matauang.matauang"))
    rate: Mapped[Decimal] = mapped_column(DECIMAL(35, 20), default=0)
    item_code: Mapped[str] = mapped_column("kodeitem", String(100), ForeignKey("tbl_item.kodeitem"))
    amount: Mapped[Decimal] = mapped_column("jumlahdasar", DECIMAL(20, 3), default=0)
    unit: Mapped[str] = mapped_column("satuandasar", String(50))
    price: Mapped[Decimal] = mapped_column("hargadasar", DECIMAL(35, 20), default=0)
    item_in: Mapped[Decimal] = mapped_column("masuk", DECIMAL(20, 3), default=0)
    item_out: Mapped[Decimal] = mapped_column("keluar", DECIMAL(20, 3), default=0)
    item_remainder: Mapped[Decimal] = mapped_column("sisa", DECIMAL(20, 3), default=0)
    office: Mapped["Office"] = relationship(back_populates="inventory_in")
    currency: Mapped["Currency"] = relationship(back_populates="inventory_in")
    item: Mapped["Item"] = relationship(back_populates="inventory_in")


class InventoryOut(BaseModel):
    """Inventory Out model for storing Outgoing of Inventories information"""

    __tablename__ = "tbl_item_ik"

    detail_id: Mapped[str] = mapped_column("iddetail", String(150), primary_key=True, nullable=False)
    detail_trs_id: Mapped[str] = mapped_column("iddetailtrs", String(150))
    no_transaction: Mapped[str] = mapped_column("notransaksi", String(100))
    office_code: Mapped[str] = mapped_column("kodekantor", String(50), ForeignKey("tbl_kantor.kodekantor"))
    date: Mapped[datetime] = mapped_column("tanggal", DateTime, server_default=func.now(), onupdate=func.now())
    type: Mapped[str] = mapped_column("tipe", String(20))
    item_code: Mapped[str] = mapped_column("kodeitem", String(100), ForeignKey("tbl_item.kodeitem"))
    amount: Mapped[Decimal] = mapped_column("jumlahdasar", DECIMAL(20, 3), default=0)
    unit: Mapped[str] = mapped_column("satuandasar", String(50))
    price: Mapped[Decimal] = mapped_column("hargadasar", DECIMAL(35, 20), default=0)
    number_of_return: Mapped[Decimal] = mapped_column("jmlretur", DECIMAL(20, 3), default=0)
    no_serial: Mapped[str] = mapped_column("noserial", String(255))
    office: Mapped["Office"] = relationship(back_populates="inventory_out")
    item: Mapped["Item"] = relationship(back_populates="inventory_out")
