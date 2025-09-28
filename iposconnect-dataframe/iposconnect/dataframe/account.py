from ibis import Table, BaseBackend

from .base import BaseTable


class Account(BaseTable):
    def extract(self) -> Table:
        self.table = self._backend.table("tbl_perkiraan")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    account_code="kodeacc",
                    account_name="namaacc",
                    currency="matauang",
                    group="kelompok",
                )
            )
        )

        self.table = (
            self.table.select("account_code", "account_name", "currency", "group")
        )

        return self.table

    def load(self) -> Table:
        return self.transform()


class Emoney(BaseTable):
    def extract(self) -> Table:
        self.table = self._backend.table("tbl_emoney")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    kode_emoney="kodeprod",
                    nama_emoney="namaprod",
                    acc_emoney="acc_prod",
                )
            )
        )

        return self.table

    def load(self) -> Table:
        return self.transform()


class Journal(BaseTable):
    def __init__(self, backend: BaseBackend = None, table: Table = None):
        super().__init__(backend, table)
        self._account = None

    def extract(self) -> Table:
        self.table = self._backend.table("tbl_accjurnal")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    date="tanggal",
                    no_transaction="notransaksi",
                    sequence="nourut",
                    account_code="kodeacc",
                    amount="jumlah",
                    position="posisi",
                    debit="debet",
                    credit="kredit",
                    office_code="kantor",
                )
            )
        )

        self.table = (
            self.table.mutate(
                date=self.table.date.cast("date"),
                account_code=self.table.account_code.cast("string"),
                amount=self.table.amount.cast("decimal(19, 2)"),
                debit=self.table.debit.cast("decimal(19, 2)"),
                credit=self.table.credit.cast("decimal(19, 2)"),
            )
        )

        account = Account(self._backend)
        self._account = account.load()

        self.table = (
            self.table.join(
                self._account,
                [self.table.account_code == self._account.account_code]
            )
        )

        self.table = (
            self.table.select("date", "no_transaction", "sequence", "account_code",
                              "account_name", "amount", "currency", "position",
                              "debit", "credit", "group", "office_code")
            .order_by("date")
        )

        return self.table

    def load(self) -> Table:
        self.table = self.transform()

        if self._is_between:
            self.table = self.table.filter(
                self.table.date.between(self._start_date, self._end_date)
            )

        return self.table

    class _Account():
        def __init__(self, table: Table, account: Table):
            self.table = table
            self._account = account

            self.table = self.table.group_by("account_code", "position").aggregate(
                debit=self.table.debit.sum(),
                credit=self.table.credit.sum(),
            )

            self.table = self.table.join(self._account, [self.table.account_code == self._account.account_code])

        def assets(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def currentAssets(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def cashAndBank(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-11")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def pettyCash(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1110")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def accountsReceivable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-12")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def receivable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1210")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def creditCardReceivables(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1220")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def emoneyReceivables(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-122X01")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def inventory(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-13")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def inventoryOfGoods(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1301")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def purchaseDiscountAndCost(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1390")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def purchaseTax(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-14")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def inputVAT(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1410")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def prepaidTaxes(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1421")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def advancePayment(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-9")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def purchaseOrderDownPayment(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-9100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def liabilities(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def currentLiabilities(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def operationalDebt(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-11")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def accountsPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1101")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def creditCardDebt(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1130")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def consignmentDebt(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1140")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def nonOperationalDebt(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-2")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def prepaidIncome(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-3")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def salesOrderAdvance(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-3100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def outputVAT(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-4110")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def taxPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-4120")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def salaryPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-5000")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def revenues(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def revenueByTrade(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-1100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def salesDiscount(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-1500")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def cost(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-1700")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def revenueByService(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-2000")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def costOfGoodsSold(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-1100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def miscellaneousCost(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def debtDeduction(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-1200")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def lossOfReceivable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def stockOpname(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2200")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def incomingItem(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2201")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def outgoingItem(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2202")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenses(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByGeneral(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-1")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByMarketing(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-2")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseBySalary(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-3")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByOperational(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-4")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByDepreciation(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-5")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByNonInventory(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-9")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def socialResponsibility(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("8-7")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def charity(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("8-7001")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

    class _Income():
        def __init__(self, _account: BaseTable):
            self._account = _account

        def totalRevenue(self):
            return self._account.revenues().total_amount.as_scalar()

        def totalCOGS(self):
            costOfGoodsSold = self._account.costOfGoodsSold().total_amount.as_scalar()
            debtDeduction = self._account.debtDeduction().total_amount.as_scalar()
            return costOfGoodsSold + debtDeduction

        def totalMiscellaneousCost(self):
            lossOfReceivable = self._account.lossOfReceivable().total_amount.as_scalar()
            incomingItem = self._account.incomingItem().total_amount.as_scalar()
            outgoingItem = self._account.outgoingItem().total_amount.as_scalar()

            return lossOfReceivable + incomingItem + outgoingItem

        def totalExpense(self):
            return self._account.expenses().total_amount.as_scalar()

        def grossProfit(self):
            return self.totalRevenue() - (self.totalCOGS() + self.totalMiscellaneousCost())

        def netProfit(self):
            return self.grossProfit() - self.totalExpense()

    class _BalanceSheet():
        def __init__(self, _account: BaseTable):
            self._account = _account

        def currentAssets(self):
            cashAndBank = self._account.cashAndBank().total_amount.as_scalar()
            accountsReceivable = self._account.accountsReceivable().total_amount.as_scalar()
            purchaseTax = self._account.purchaseTax().total_amount.as_scalar()
            inventory = self._account.inventory().total_amount.as_scalar()

            return cashAndBank + accountsReceivable + purchaseTax + inventory

        def totalAssets(self):
            return self._account.assets().total_amount.as_scalar()

        def currentLiabilities(self):
            operationalDebt = self._account.operationalDebt().total_amount.as_scalar()
            salaryPayable = self._account.salaryPayable().total_amount.as_scalar()

            return operationalDebt + salaryPayable

        def totalLiabilities(self):
            return self._account.liabilities().total_amount.as_scalar()

        def retainedEarning(self):
            return self.totalAssets() - self.totalLiabilities()

        def totalEquites(self):
            return self.retainedEarning() + 0

    class _FinancialRatio():
        def __init__(self, _account: BaseTable, _income: BaseTable, _balanceSheet: BaseTable):
            self._account = _account
            self._income = _income
            self._balanceSheet = _balanceSheet

        def currentRatio(self):
            currentAssets = self._balanceSheet.currentAssets().to_pandas()
            currentLiabilities = self._balanceSheet.currentLiabilities().to_pandas()

            if (currentAssets != 0) and (currentLiabilities != 0):
                return currentAssets / currentLiabilities
            else:
                return 0

        def quickRatio(self):
            inventory = self._income._account.inventory().total_amount.as_scalar().to_pandas()
            currentAssets = self._balanceSheet.currentAssets().to_pandas()
            currentLiabilities = self._balanceSheet.currentLiabilities().to_pandas()

            if ((currentAssets - inventory) != 0) and (currentLiabilities != 0):
                return (currentAssets - inventory) / currentLiabilities
            else:
                return 0

        def grossProfitMarginRatio(self):
            grossProfit = self._income.grossProfit().to_pandas()
            totalRevenue = self._income.totalRevenue().to_pandas()

            # Measure of a company's overall profitability from gross profit.
            if (grossProfit != 0) and (totalRevenue != 0):
                return (grossProfit / totalRevenue)
            else:
                return 0

        def netProfitMarginRatio(self):
            netProfit = self._income.netProfit().to_pandas()
            totalRevenue = self._income.totalRevenue().to_pandas()

            # Measure of a company's overall profitability from net profit.
            if (netProfit != 0) and (totalRevenue != 0):
                return (netProfit / totalRevenue)
            else:
                return 0

        def operatingMarginRatio(self):
            costOfGoodsSold = self._income._account.costOfGoodsSold().total_amount.as_scalar().to_pandas()
            totalExpense = self._income.totalExpense().to_pandas()
            totalRevenue = self._income.totalRevenue().to_pandas()
            totalOperational = totalRevenue - (costOfGoodsSold + totalExpense)

            # The operating margin is an important measure of a company's overall profitability from operations.
            if (totalOperational != 0) and (totalRevenue != 0):
                return (totalOperational / totalRevenue)
            else:
                return 0

        def debtToAssetRatio(self):
            assets = self._account.assets().total_amount.as_scalar().to_pandas()
            operationalDebt = self._account.operationalDebt().total_amount.as_scalar().to_pandas()
            nonOperationalDebt = self._account.nonOperationalDebt().total_amount.as_scalar().to_pandas()
            totalDebt = operationalDebt + nonOperationalDebt

            if (totalDebt != 0) and (assets != 0):
                return (totalDebt / assets)
            else:
                return 0

        def socialResponsibilityToProfitRatio(self):
            socialResponsibility = self._account.socialResponsibility().total_amount.as_scalar().to_pandas()
            netProfit = self._income.netProfit().to_pandas()

            if (socialResponsibility != 0) and (netProfit != 0):
                return (socialResponsibility / netProfit)
            else:
                return 0

    def account(self):
        return Journal._Account(self.load(), self._account)

    def income(self):
        return Journal._Income(self.account())

    def balanceSheet(self):
        return Journal._BalanceSheet(self.account())

    def financialRatio(self):
        return Journal._FinancialRatio(self.account(), self.income(), self.balanceSheet())


class JournalV5(BaseTable):
    def __init__(self, backend: BaseBackend = None, table: Table = None):
        super().__init__(backend, table)
        self._account = None

    def extract(self) -> Table:
        self.table = self._backend.table("tbl_accjurnal")
        return self.table

    def transform(self) -> Table:
        self.table = self.extract()

        self.table = (
            self.table.rename(
                dict(
                    date="tanggal",
                    no_transaction="notransaksi",
                    sequence="nourut",
                    account_code="kodeacc",
                    amount="jumlah",
                    position="posisi",
                    debit="debet",
                    credit="kredit",
                    office_code="kantor",
                )
            )
        )

        self.table = (
            self.table.mutate(
                date=self.table.date.cast("date"),
                account_code=self.table.account_code.cast("string"),
                amount=self.table.amount.cast("decimal(19, 2)"),
                debit=self.table.debit.cast("decimal(19, 2)"),
                credit=self.table.credit.cast("decimal(19, 2)"),
            )
        )

        account = Account(self._backend)
        self._account = account.load()

        self.table = (
            self.table.join(
                self._account,
                [self.table.account_code == self._account.account_code]
            )
        )

        self.table = (
            self.table.select("date", "no_transaction", "sequence", "account_code",
                              "account_name", "amount", "currency", "position",
                              "debit", "credit", "group", "office_code")
            .order_by("date")
        )

        return self.table

    def load(self) -> Table:
        self.table = self.transform()

        if self._is_between:
            self.table = self.table.filter(
                self.table.date.between(self._start_date, self._end_date)
            )

        return self.table

    class _Account():
        def __init__(self, table: Table, account: Table):
            self.table = table
            self._account = account

            self.table = self.table.group_by("account_code", "position").aggregate(
                debit=self.table.debit.sum(),
                credit=self.table.credit.sum(),
            )

            self.table = self.table.join(self._account, [self.table.account_code == self._account.account_code])

        def assets(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def currentAssets(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def cashAndBank(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-11")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def pettyCash(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1110")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def accountsReceivable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-12")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def receivable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1210")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def creditCardReceivables(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1220")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def emoneyReceivables(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-122X01")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def purchaseTax(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-14")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def inputVAT(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1410")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def prepaidTaxes(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-1421")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def inventory(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-20")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def inventoryOfGoods(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-2010")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def purchaseDiscountAndCost(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-2390")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def assembly(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-3")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def inventoryOfGoodsInTheAssemblyProcess(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-3010")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def consignmentOut(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-4")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def consignmentItemsOut(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-4010")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def fixedAssets(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-5")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def advancePayment(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-9")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def purchaseOrderDownPayment(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-9100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def depositFundsWithSuppliers(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1-9101")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def consignmentDepositFundsGoToTheSupplier(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("1.9699X01")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def liabilities(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def currentLiabilities(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def operationalDebt(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-11")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def accountsPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1101")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def creditCardDebt(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1130")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def consignmentDebt(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1140")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def salaryPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1200")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def salesPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1300")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def assemblyProcess(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-15")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def assemblyProcessSalariesPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1501")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def assemblyProcessOverheadCostsPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-1510")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def nonOperationalDebt(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-2")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def deliveryPostagePayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-2100X01")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def prepaidIncome(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-3")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def salesOrderAdvance(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-3100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def customerDeposit(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-3101")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def consignmentCustomerDepositOut(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-3699X01")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def outputVAT(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-4110")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def taxPayable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-4120")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def incomingConsignmentGoods(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-6")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def consignmentItems(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("2-6100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def revenues(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def revenueByTrade(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-1100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def revenueByConsignment(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-1101")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def salesDiscount(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-1500")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def salesReturns(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-1600")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def cost(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-1700")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def revenueByService(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("4-2000")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def costOfGoodsSold(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-1300")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def purchaseDiscount(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-199X01")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def miscellaneousCost(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def lossOfReceivable(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2100")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def stockOpname(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2200")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.credit.sum() - self.table.debit.sum())
                ).fill_null(0)
            )

        def incomingItem(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2201")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def outgoingItem(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("5-2202")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenses(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByGeneral(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-1")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByMarketing(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-2")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseBySalary(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-3")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByOperational(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-4")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByDepreciation(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-5")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def expenseByNonInventory(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("6-9")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def socialResponsibility(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("8-7")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

        def charity(self):
            return (
                self.table.filter(
                    self.table.account_code.contains("8-7001")
                ).aggregate(
                    total_debit=self.table.debit.sum(),
                    total_credit=self.table.credit.sum(),
                    total_amount=(self.table.debit.sum() - self.table.credit.sum())
                ).fill_null(0)
            )

    class _Income():
        def __init__(self, _account: BaseTable):
            self._account = _account

        def totalRevenue(self):
            return self._account.revenues().total_amount.as_scalar()

        def totalCOGS(self):
            costOfGoodsSold = self._account.costOfGoodsSold().total_amount.as_scalar()
            purchaseDiscount = self._account.purchaseDiscount().total_amount.as_scalar()
            return costOfGoodsSold + purchaseDiscount

        def totalMiscellaneousCost(self):
            lossOfReceivable = self._account.lossOfReceivable().total_amount.as_scalar()
            incomingItem = self._account.incomingItem().total_amount.as_scalar()
            outgoingItem = self._account.outgoingItem().total_amount.as_scalar()

            return lossOfReceivable + incomingItem + outgoingItem

        def totalExpense(self):
            return self._account.expenses().total_amount.as_scalar()

        def grossProfit(self):
            return self.totalRevenue() - (self.totalCOGS() + self.totalMiscellaneousCost())

        def netProfit(self):
            return self.grossProfit() - self.totalExpense()

    class _BalanceSheet():
        def __init__(self, _account: BaseTable):
            self._account = _account

        def currentAssets(self):
            cashAndBank = self._account.cashAndBank().total_amount.as_scalar()
            accountsReceivable = self._account.accountsReceivable().total_amount.as_scalar()
            purchaseTax = self._account.purchaseTax().total_amount.as_scalar()
            inventory = self._account.inventory().total_amount.as_scalar()

            return cashAndBank + accountsReceivable + purchaseTax + inventory

        def totalAssets(self):
            return self._account.assets().total_amount.as_scalar()

        def currentLiabilities(self):
            operationalDebt = self._account.operationalDebt().total_amount.as_scalar()
            salaryPayable = self._account.salaryPayable().total_amount.as_scalar()
            salesPayable = self._account.salesPayable().total_amount.as_scalar()
            assemblyProcess = self._account.assemblyProcess().total_amount.as_scalar()

            return operationalDebt + salaryPayable + salesPayable + assemblyProcess

        def totalLiabilities(self):
            return self._account.liabilities().total_amount.as_scalar()

        def retainedEarning(self):
            return self.totalAssets() - self.totalLiabilities()

        def totalEquites(self):
            return self.retainedEarning() + 0

    class _FinancialRatio():
        def __init__(self, _account: BaseTable, _income: BaseTable, _balanceSheet: BaseTable):
            self._account = _account
            self._income = _income
            self._balanceSheet = _balanceSheet

        def currentRatio(self):
            currentAssets = self._balanceSheet.currentAssets().to_pandas()
            currentLiabilities = self._balanceSheet.currentLiabilities().to_pandas()

            if (currentAssets != 0) and (currentLiabilities != 0):
                return currentAssets / currentLiabilities
            else:
                return 0

        def quickRatio(self):
            inventory = self._income._account.inventory().total_amount.as_scalar().to_pandas()
            currentAssets = self._balanceSheet.currentAssets().to_pandas()
            currentLiabilities = self._balanceSheet.currentLiabilities().to_pandas()

            if ((currentAssets - inventory) != 0) and (currentLiabilities != 0):
                return (currentAssets - inventory) / currentLiabilities
            else:
                return 0

        def grossProfitMarginRatio(self):
            grossProfit = self._income.grossProfit().to_pandas()
            totalRevenue = self._income.totalRevenue().to_pandas()

            # Measure of a company's overall profitability from gross profit.
            if (grossProfit != 0) and (totalRevenue != 0):
                return (grossProfit / totalRevenue)
            else:
                return 0

        def netProfitMarginRatio(self):
            netProfit = self._income.netProfit().to_pandas()
            totalRevenue = self._income.totalRevenue().to_pandas()

            # Measure of a company's overall profitability from net profit.
            if (netProfit != 0) and (totalRevenue != 0):
                return (netProfit / totalRevenue)
            else:
                return 0

        def operatingMarginRatio(self):
            costOfGoodsSold = self._income._account.costOfGoodsSold().total_amount.as_scalar().to_pandas()
            totalExpense = self._income.totalExpense().to_pandas()
            totalRevenue = self._income.totalRevenue().to_pandas()
            totalOperational = totalRevenue - (costOfGoodsSold + totalExpense)

            # The operating margin is an important measure of a company's overall profitability from operations.
            if (totalOperational != 0) and (totalRevenue != 0):
                return (totalOperational / totalRevenue)
            else:
                return 0

        def debtToAssetRatio(self):
            assets = self._account.assets().total_amount.as_scalar().to_pandas()
            operationalDebt = self._account.operationalDebt().total_amount.as_scalar().to_pandas()
            nonOperationalDebt = self._account.nonOperationalDebt().total_amount.as_scalar().to_pandas()
            totalDebt = operationalDebt + nonOperationalDebt

            if (totalDebt != 0) and (assets != 0):
                return (totalDebt / assets)
            else:
                return 0

        def socialResponsibilityToProfitRatio(self):
            socialResponsibility = self._account.socialResponsibility().total_amount.as_scalar().to_pandas()
            netProfit = self._income.netProfit().to_pandas()

            if (socialResponsibility != 0) and (netProfit != 0):
                return (socialResponsibility / netProfit)
            else:
                return 0

    def account(self):
        return JournalV5._Account(self.load(), self._account)

    def income(self):
        return JournalV5._Income(self.account())

    def balanceSheet(self):
        return JournalV5._BalanceSheet(self.account())

    def financialRatio(self):
        return JournalV5._FinancialRatio(self.account(), self.income(), self.balanceSheet())