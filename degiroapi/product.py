from datetime import datetime


class Product:
    def __init__(self, product):
        self.__id = product['id']
        self.__name = product['name']
        self.__isin = product['isin']
        self.__symbol = product['symbol']
        self.__currency = product['currency']
        self.__product_type = product['productTypeId']
        self.__tradable = product['tradable']
        self.__close_price = product.get('closePrice')
        close_price_date = product.get('closePriceDate')
        self.__close_price_date = datetime.strptime(close_price_date, '%Y-%m-%d').date() if close_price_date else None

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def isin(self):
        return self.__isin

    @property
    def symbol(self):
        return self.__symbol

    @property
    def currency(self):
        return self.__currency

    @property
    def product_type(self):
        return self.__product_type

    @property
    def tradable(self):
        return self.__tradable

    @property
    def close_price(self):
        return self.__close_price

    @property
    def close_price_date(self):
        return self.__close_price_date
