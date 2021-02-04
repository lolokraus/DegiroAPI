class Order:
    class Type:
        LIMIT = 0
        STOPLIMIT = 1
        MARKET = 2
        STOPLOSS = 3
    class Time:
        DAY = 1
        GTC = 3  # Good-Til-Cancelled
