from degiroapi.datatypes import Data
from datetime import datetime, timedelta
from degiroapi import DeGiro
from degiroapi.product import Product
from degiroapi.utils import pretty_json
from degiroapi.order import Order

# login
degiro = DeGiro()
degiro.login("username", "password")

# print the current cash funds
cachfunds = degiro.getdata(Data.Type.CACHFUNDS)
for data in cachfunds:
    print(data)

# print the current portfolio
portfolio = degiro.getdata(Data.Type.PORTFOLIO)
for data in portfolio:
    print(data)

# output one search result
products = degiro.search_products('Pfizer')
print(Product(products[0]).id)

# output multiple search result
products = degiro.search_products('Pfizer', 3)
print(Product(products[0]).id)
print(Product(products[1]).id)
print(Product(products[2]).id)

# print transactions
transactions = degiro.transactions(datetime(2019, 1, 1), datetime.now())
print(pretty_json(transactions))

# print order history (maximum timespan 90 days)
orders = degiro.orders(datetime.now() - timedelta(days=90), datetime.now())
print(pretty_json(orders))

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

# the stop loss price has to be higher than the current price, when current price reaches the stoploss price the order is places
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









