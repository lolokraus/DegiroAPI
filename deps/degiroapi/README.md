# DegiroAPI
An unofficial API for the trading platform Degiro written in Python with the ability to get real time data and historical data for products. 

## Getting Started

### Installing
```
pip install degiroapi
```
### Dependecies
```
pip install requests
```
### Imports
```
import degiroapi
from degiroapi.product import Product
from degiroapi.order import Order
from degiroapi.utils import pretty_json
```
### Logging into your account
```
degiro = degiroapi.DeGiro()
degiro.login("username", "password")
```
### Logging out

```
degiro.logout()
```

## Available Functions
* login
* logout
* getdata
* search_products
* product_info
* transactions
* orders
* delete_order
* real_time_price
* get_stock_list
* buyorder
* sellorder
## getdata
Printing your current cach funds:
```
cashfunds = degiro.getdata(degiroapi.Data.Type.CASHFUNDS)
for data in cashfunds:
    print(data)
```
Printing your current portfolio, argument True to filter out products with a size of 0, False or no Argument to show all:
```
portfolio = degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
for data in portfolio:
    print(data)
```
## search_products
Searching for a product:
```
products = degiro.search_products('Pfizer')
print(Product(products[0]).id)
```
## product_info
Printing info for a specified product ID:
```
info = degiro.product_info(331823)
print(info["id"], info["name"], info["currency"], info["closePrice"])
```
## transactions
Printing your transactions in a given time interval:
```
from datetime import datetime, timedelta

transactions = degiro.transactions(datetime(2019, 1, 1), datetime.now())
print(pretty_json(transactions))
```
## orders
Printing your order history(the maximum timespan is 90 days)
With argument True, this function only returns open orders
```
from datetime import datetime, timedelta

orders = degiro.orders(datetime.now() - timedelta(days=90), datetime.now())
print(pretty_json(orders))

orders = degiro.orders(datetime.now() - timedelta(days=90), datetime.now(), True)
print(pretty_json(orders))
```

## delete_order
Deleting an open order with the orderId
```
orders = degiro.orders(datetime.now() - timedelta(days=1), datetime.now(), True)
degiro.delete_order(orders[0]['orderId'])
```
```
degiro.delete_order("f278d56f-eaa0-4dc7-b067-45c6b4b3d74f")
```

## real_time_price
Get the real time price and the historical data of a stock:
```
products = degiro.search_products('nrz')
# Interval can be set to One_Day, One_Week, One_Month, Three_Months, Six_Months, One_Year, Three_Years, Five_Years, Max
realprice = degiro.real_time_price(Product(products[0]).id, degiroapi.Interval.Type.One_Day)

# getting the real time price
print(realprice[0]['data']['lastPrice'])
print(pretty_json(realprice[0]['data']))

# getting historical data
print(realprice[1]['data'])
```

## get_stock_list
Get the symbols of the S&P500 stocks:
```
sp5symbols = []
products = degiro.get_stock_list(14, 846)
for product in products:
    sp5symbols.append(Product(product).symbol)
```
Get the symbols of the german30 stocks:
```
daxsymbols = []
products = degiro.get_stock_list(6, 906)
for product in products:
    daxsymbols.append(Product(product).symbol)
```
## buyorder
Placing a buy order is dependent on the order Type:

### Limit order 
You have to set a limit order price to which the order gets executed.
**arguments**: order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for unlimited, size, limit(the limit price)
```
degiro.buyorder(Order.Type.LIMIT, Product(products[0]).id, 3, 1, 30)
```

### StopLimit order
Sets a limit order when the stoploss price is reached (not bought for more than the limit at the stop loss price):
**arguments**: order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size, limit(the limit price), stop_loss(stop loss price)
```
degiro.buyorder(Order.Type.STOPLIMIT, Product(products[0]).id, 3, 1, 38, 38)
```

### Market order
Bought at the market price:
**arguments**: order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size
```
degiro.buyorder(Order.Type.MARKET, Product(products[0]).id, 3, 1)
```

### StopLoss order
The stop loss price has to be higher than the current price, when current price reaches the stoploss price the order is placed:
**arguments**: order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size
```
degiro.buyorder(Order.Type.STOPLOSS, Product(products[0]).id, 3, 1, None, 38)
```

## sellorder
Placing a sell order is dependent on the order Type:
Equivalent to the buy orders:
```
degiro.sellorder(Order.Type.LIMIT, Product(products[0]).id, 3, 1, 40)
```

```
degiro.sellorder(Order.Type.STOPLIMIT, Product(products[0]).id, 3, 1, 37, 38)
```

```
degiro.sellorder(Order.Type.MARKET, Product(products[0]).id, 3, 1)
```

```
degiro.sellorder(Order.Type.STOPLOSS, Product(products[0]).id, 3, 1, None, 38)
```


## Usage
For documented examples see [examples.py](https://github.com/lolokraus/DegiroAPI/blob/master/examples/examples.py)




