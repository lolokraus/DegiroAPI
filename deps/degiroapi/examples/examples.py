from deps import degiroapi
from deps.degiroapi.product import Product
from deps.degiroapi import Order
from deps.degiroapi.utils import pretty_json

from datetime import datetime, timedelta

# login
degiro = degiroapi.DeGiro()
degiro.login("username", "password")

# logout
degiro.logout()

# print the current cash funds
cashfunds = degiro.getdata(degiroapi.Data.Type.CASHFUNDS)
for data in cashfunds:
    print(data)

# print the current portfolio (True to filter Products with size 0, False to show all)
portfolio = degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
for data in portfolio:
    print(data)

# output one search result
products = degiro.search_products('Pfizer')
print(Product(products[0]).id)
print(Product(products[0]).name)
print(Product(products[0]).symbol)
print(Product(products[0]).isin)
print(Product(products[0]).currency)
print(Product(products[0]).product_type)
print(Product(products[0]).tradable)
print(Product(products[0]).close_price)
print(Product(products[0]).close_price_date)

# output multiple search result
products = degiro.search_products('Pfizer', 3)
print(Product(products[0]).id)
print(Product(products[1]).id)
print(Product(products[2]).id)

# printing info for a specified product ID:
info = degiro.product_info(5322419)
print(info["id"], info["name"], info["currency"], info["closePrice"])

# print transactions
transactions = degiro.transactions(datetime(2019, 1, 1), datetime.now())
print(pretty_json(transactions))

# print order history (maximum timespan 90 days)
orders = degiro.orders(datetime.now() - timedelta(days=90), datetime.now())
print(pretty_json(orders))

# printing order history (maximum timespan 90 days), with argument True return only open orders
orders = degiro.orders(datetime.now() - timedelta(days=90), datetime.now(), True)
print(pretty_json(orders))

# deleting an open order
orders = degiro.orders(datetime.now() - timedelta(days=1), datetime.now(), True)
degiro.delete_order(orders[0]['orderId'])

degiro.delete_order("f278d56f-eaa0-4dc7-b067-45c6b4b3d74f")

# getting realtime and historical data from a stock
products = degiro.search_products('nrz')

# Interval can be set to One_Day, One_Week, One_Month, Three_Months, Six_Months, One_Year, Three_Years, Five_Years, Max
realprice = degiro.real_time_price(Product(products[0]).id, degiroapi.Interval.Type.One_Day)

# reatime data
print(realprice[0]['data']['lastPrice'])
print(pretty_json(realprice[0]['data']))

# historical data
print(realprice[1]['data'])

# get s&p 500 stock list
sp5symbols = []
products = degiro.get_stock_list(14, 846)
for product in products:
    sp5symbols.append(Product(product).symbol)

# get german30 stock list
daxsymbols = []
products = degiro.get_stock_list(6, 906)
for product in products:
    daxsymbols.append(Product(product).symbol)

# placing an order(dependent on the order type)
# set a limit order price to which the order gets executed
# order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for unlimited, size, limit(the limit price)
degiro.buyorder(Order.Type.LIMIT, Product(products[0]).id, 3, 1, 30)

# sets a limit order when the stoploss price is reached(not bought for more than the limit at the stop loss price)
# order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size, limit(the limit price), stop_loss(stop loss price)
degiro.buyorder(Order.Type.STOPLIMIT, Product(products[0]).id, 3, 1, 38, 38)

# order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size
degiro.buyorder(Order.Type.MARKET, Product(products[0]).id, 3, 1)

# the stop loss price has to be higher than the current price, when current price reaches the stoploss price the order is placed
# order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size, don't change none, stop_loss(stop loss price)
degiro.buyorder(Order.Type.STOPLOSS, Product(products[0]).id, 3, 1, None, 38)

# selling a product
# order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for unlimited, size, limit(the limit price)
degiro.sellorder(Order.Type.LIMIT, Product(products[0]).id, 3, 1, 40)

# order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size, limit(the limit price), stop_loss(stop loss price)
degiro.sellorder(Order.Type.STOPLIMIT, Product(products[0]).id, 3, 1, 37, 38)

# order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size
degiro.sellorder(Order.Type.MARKET, Product(products[0]).id, 3, 1)

# order type, product id, execution time type (either 1 for "valid on a daily basis", or 3 for "unlimited"), size, don't change none, stop_loss(stop loss price)
degiro.sellorder(Order.Type.STOPLOSS, Product(products[0]).id, 3, 1, None, 38)
