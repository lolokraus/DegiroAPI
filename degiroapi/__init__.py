import requests, json
from degiroapi.order import Order
from degiroapi.client_info import ClientInfo
from degiroapi.datatypes import Data

class DeGiro:
    __LOGIN_URL = 'https://trader.degiro.nl/login/secure/login'
    __LOGOUT_URL = 'https://trader.degiro.nl/trading/secure/logout'

    __CLIENT_INFO_URL = 'https://trader.degiro.nl/pa/secure/client'

    __GET_STOCKS_URL = 'https://trader.degiro.nl/products_s/secure/v5/stocks'
    __PRODUCT_SEARCH_URL = 'https://trader.degiro.nl/product_search/secure/v5/products/lookup'
    __PRODUCT_INFO_URL = 'https://trader.degiro.nl/product_search/secure/v5/products/info'
    __TRANSACTIONS_URL = 'https://trader.degiro.nl/reporting/secure/v4/transactions'
    __ORDERS_URL = 'https://trader.degiro.nl/reporting/secure/v4/order-history'

    __PLACE_ORDER_URL = 'https://trader.degiro.nl/trading/secure/v5/checkOrder'
    __CONFIRM_ORDER_URL = 'https://trader.degiro.nl/trading/secure/v5/order/'

    __DATA_URL = 'https://trader.degiro.nl/trading/secure/v5/update/'

    __GET_REQUEST = 0
    __POST_REQUEST = 1

    session_id = any
    client_info = any
    confirmation_id = any

    def login(self, username, password):
        login_payload = {
            'username': username,
            'password': password,
            'isPassCodeReset': False,
            'isRedirectToMobile': False
        }
        login_response = self.__request(DeGiro.__LOGIN_URL, login_payload, request_type=DeGiro.__POST_REQUEST,
                                        error_message='Could not login.')
        self.session_id = login_response['sessionId']
        client_info_payload = {'sessionId': self.session_id}
        client_info_response = self.__request(DeGiro.__CLIENT_INFO_URL, client_info_payload,
                                              error_message='Could not get client info.')
        self.client_info = ClientInfo(client_info_response['data'])

        return client_info_response

    def logout(self):
        logout_payload = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id,
        }
        self.__request(DeGiro.__LOGOUT_URL + ';jsessionid=' + self.session_id, logout_payload, error_message='Could not log out')

    @staticmethod
    def __request(url, payload, headers=None, data=None, post_params=None, request_type=__GET_REQUEST, error_message='An error occurred.'):
        if request_type == DeGiro.__GET_REQUEST:
            response = requests.get(url, params=payload)
        elif request_type == DeGiro.__POST_REQUEST and headers and data:
            response = requests.post(url, headers=headers, params=payload, data=data)
        elif request_type == DeGiro.__POST_REQUEST and post_params:
            response = requests.post(url, params=post_params, json=payload)
        elif request_type == DeGiro.__POST_REQUEST:
            response = requests.post(url, json=payload)
        else:
            raise Exception(f'Unknown request type: {request_type}')

        if response.status_code == 200 or response.status_code == 201:
            try:
                return response.json()
            except:
                return "No data"
        else:
            raise Exception(f'{error_message} Response: {response.text}')

    def search_products(self, search_text, limit=1):
        product_search_payload = {
            'searchText': search_text,
            'limit': limit,
            'offset': 0,
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }
        return \
            self.__request(DeGiro.__PRODUCT_SEARCH_URL, product_search_payload,
                           error_message='Could not get products.')[
                'products']

    def product_info(self, product_id):
        product_info_payload = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }
        return \
            self.__request(DeGiro.__PRODUCT_INFO_URL, 
                product_info_payload, 
                headers={'content-type': 'application/json'}, 
                data=json.dumps([str(product_id)]),
                request_type=DeGiro.__POST_REQUEST,
                error_message='Could not get product info.')['data'][str(product_id)]

    def transactions(self, from_date, to_date, group_transactions=False):
        transactions_payload = {
            'fromDate': from_date.strftime('%d/%m/%Y'),
            'toDate': to_date.strftime('%d/%m/%Y'),
            'group_transactions_by_order': group_transactions,
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }
        return \
            self.__request(DeGiro.__TRANSACTIONS_URL, transactions_payload,
                           error_message='Could not get transactions.')[
                'data']

    def orders(self, from_date, to_date):
        orders_payload = {
            'fromDate': from_date.strftime('%d/%m/%Y'),
            'toDate': to_date.strftime('%d/%m/%Y'),
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }
        # max 90 days
        if (to_date - from_date).days > 90:
            raise Exception('The maximum timespan is 90 days')
        return self.__request(DeGiro.__ORDERS_URL, orders_payload, error_message='Could not get orders.')['data']

    @staticmethod
    def filtercashfunds(cashfunds):
        data = []
        for item in cashfunds['cashFunds']['value']:
            if item['value'][2]['value'] != 0:
                data.append(item['value'][1]['value'] + " " + str(item['value'][2]['value']))
        return data

    @staticmethod
    def filterportfolio(portfolio):
        data = []
        for item in portfolio['portfolio']['value']:
            positionType = size = price = value = breakEvenPrice = None
            for i in item['value']:
                positionType = i['value'] if i['name'] == 'positionType' else positionType
                size = i['value'] if i['name'] == 'size' else size
                price = i['value'] if i['name'] == 'price' else price
                value = i['value'] if i['name'] == 'value' else value
                breakEvenPrice = i['value'] if i['name'] == 'breakEvenPrice' else breakEvenPrice
            data.append({
                "id": item['id'],
                "positionType": positionType,
                "size": size,
                "price": price,
                "value": value,
                "breakEvenPrice": breakEvenPrice
                })
        return data

    def getdata(self, datatype):
        data_payload = {
            datatype: 0
        }

        if datatype == Data.Type.CASHFUNDS:
            return self.filtercashfunds(
                self.__request(DeGiro.__DATA_URL + str(self.client_info.account_id) + ';jsessionid=' + self.session_id,
                               data_payload, error_message='Could not get data'))
        elif datatype == Data.Type.PORTFOLIO:
            return self.filterportfolio(
                self.__request(DeGiro.__DATA_URL + str(self.client_info.account_id) + ';jsessionid=' + self.session_id,
                               data_payload, error_message='Could not get data'))
        else:
            return self.__request(
                DeGiro.__DATA_URL + str(self.client_info.account_id) + ';jsessionid=' + self.session_id, data_payload, error_message='Could not get data')

    def buyorder(self, orderType, productId, timeType, size, limit=None, stop_loss=None):
        place_buy_order_params = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id,
        }
        place_buy_order_payload = {
            'buySell': "BUY",
            'orderType': orderType,
            'productId': productId,
            'timeType': timeType,
            'size': size,
            'price': limit,
            'stopPrice': stop_loss,
        }
        if orderType != Order.Type.STOPLIMIT and orderType != Order.Type.MARKET \
                and orderType != Order.Type.LIMIT and orderType != Order.Type.STOPLOSS:
            raise Exception('Invalid order type')

        if timeType != 1 and timeType != 3:
            raise Exception('Invalid time type')

        place_check_order_response = self.__request(DeGiro.__PLACE_ORDER_URL + ';jsessionid=' + self.session_id,
                                                    place_buy_order_payload, place_buy_order_params,
                                                    request_type=DeGiro.__POST_REQUEST,
                                                    error_message='Could not place order')

        self.confirmation_id = place_check_order_response['data']['confirmationId']

        self.__request(DeGiro.__CONFIRM_ORDER_URL + self.confirmation_id + ';jsessionid=' + self.session_id,
                       place_buy_order_payload, place_buy_order_params, request_type=DeGiro.__POST_REQUEST,
                       error_message='Could not confirm order')

    def sellorder(self, orderType, productId, timeType, size, limit=None, stop_loss=None):
        place_sell_order_params = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id,
        }
        place_sell_order_payload = {
            'buySell': "SELL",
            'orderType': orderType,
            'productId': productId,
            'timeType': timeType,
            'size': size,
            'price': limit,
            'stopPrice': stop_loss,
        }
        if orderType != Order.Type.STOPLIMIT and orderType != Order.Type.MARKET \
                and orderType != Order.Type.LIMIT and orderType != Order.Type.STOPLOSS:
            raise Exception('Invalid order type')

        if timeType != 1 and timeType != 3:
            raise Exception('Invalid time type')

        place_check_order_response = self.__request(DeGiro.__PLACE_ORDER_URL + ';jsessionid=' + self.session_id,
                                                    place_sell_order_payload, place_sell_order_params,
                                                    request_type=DeGiro.__POST_REQUEST,
                                                    error_message='Could not place order')

        self.confirmation_id = place_check_order_response['data']['confirmationId']

        self.__request(DeGiro.__CONFIRM_ORDER_URL + self.confirmation_id + ';jsessionid=' + self.session_id,
                       place_sell_order_payload, place_sell_order_params, request_type=DeGiro.__POST_REQUEST,
                       error_message='Could not confirm order')

    def get_stock_list(self, indexId, stockCountryId):
        stock_list_params = {
            'indexId': indexId,
            'stockCountryId': stockCountryId,
            'offset': 0,
            'limit': None,
            'requireTotal': "true",
            'sortColumns': "name",
            'sortTypes': "asc",
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }
        return self.__request(DeGiro.__GET_STOCKS_URL, stock_list_params, error_message='Could not get stock list')[
            'products']
