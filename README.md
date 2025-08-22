## iPos Desktop Connect

##### Python API for [iPos Dekstop](https://inspirasi.biz/downloads) - The best desktop-based Point of Sales software.
API Wrapper uses [Ibis](https://ibis-project.org/) dataframe library, simplifying data transformation to Pandas, CSV, JSON, etc.

### How to install

```
git clone https://github.com/DeeloaSociety/iposconnect_py iposconnect
pip install -e iposconnect
```
create .env for database configuration from .example

### Create python object
```python
from iposconnect import IposConnect

iposConnect = IposConnect()
```

### Load the data
```python
# get table
iposConnect.salesInvoice().load()

# to pandas
iposConnect.salesInvoice().load().to_pandas()
```

### Data filtering and parts
```python
(
    iposConnect.salesInvoiceDetails()
    .between("2025-08-01", "2025-08-22")
    .parts()
    .revenueByItemCode()
)
```

### Support Version 5
```python
journalV5 = (
    iposConnect.journalV5()
    .between("2025-08-01", "2025-08-22")
)

# get income statement
journalV5.income().totalRevenue()
journalV5.income().netProfit()

# get financial ratio
journalV5.financialRatio().debtToAssetRatio()
journalV5.financialRatio().socialResponsibilityToProfitRatio()
```

### Build in forecast data
```python
# example of sales forecasting
sales_forecast = (
    iposConnect.salesInvoiceDetails()
    .between("2025-08-14", "2025-08-22")
    .forcast(item_kode="07-pengaha-bunga-1bks")
    .prepare(target='jumlah_item')
    .fit()
)

# get prediction table
print(sales_forecast.predict(step=3))
```

### License
MIT