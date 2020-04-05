class ClientInfo:
    def __init__(self, client_info):
        self.__account_id = client_info['intAccount']
        self.__username = client_info['username']
        self.__first_name = client_info['firstContact']['firstName']
        self.__last_name = client_info['firstContact']['lastName']
        self.__email = client_info['email']

    @property
    def account_id(self):
        return self.__account_id

    @property
    def username(self):
        return self.__username

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def email(self):
        return self.__email
