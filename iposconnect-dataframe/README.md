## iPos Desktop Connect - Dataframe

#### API wrapper uses [Ibis](https://ibis-project.org/) dataframe library, simplifying data transformation to Pandas, CSV, JSON, etc.

### How to install
To install the package, run the following command:
```shell
git clone https://github.com/DeeloaSociety/iposconnect
cd iposconnect/iposconnect-dataframe/
pip install .
```
Download from git resources:
```shell
pip install git+https://github.com/DeeloaSociety/iposconnect.git@develop#subdirectory=iposconnect-dataframe
```
create .env for database configuration from .env.example

### Create python object

```python
from iposconnect.dataframe import IposDataframe

iposDataframe = IposDataframe()
```

### Load the data
```python
# get table
iposDataframe.salesInvoice().load()

# to pandas
iposDataframe.salesInvoice().load().to_pandas()
```

### Data filtering and parts
```python
(
    iposDataframe.salesInvoiceDetails()
    .between("2025-08-01", "2025-08-22")
    .parts()
    .revenueByItemCode()
)
```

### Support Version 5
```python
journalV5 = (
    iposDataframe.journalV5()
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
    iposDataframe.salesInvoiceDetails()
    .between("2025-08-14", "2025-08-22")
    .forecast(item_kode="07-pengaha-bunga-1bks")
    .prepare(target='jumlah_item')
    .fit()
)

# get prediction table
print(sales_forecast.predict(step=3))
```

### License
MIT