from SmartApi import SmartConnect
import pyotp
from logzero import logger

# API credentials and other sensitive info
api_key = 'dzZ33rQv'
username = 'R306312'
pwd = '1515'
smartApi = SmartConnect(api_key)

# Function for generating session and placing orders
def generate_session_and_place_order():
    try:
        token = "XX2N5KOLPKRYYWQI2EZ7WANUIM"
        totp = pyotp.TOTP(token).now()  # Generate TOTP (time-based one-time password)
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    correlation_id = "abcde"
    data = smartApi.generateSession(username, pwd, totp)

    if data['status'] == False:
        logger.error(data)
    else:
        # login api call
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        
        # Fetch feed token
        feedToken = smartApi.getfeedToken()

        # Fetch User Profile
        res = smartApi.getProfile(refreshToken)
        smartApi.generateToken(refreshToken)
        res = res['data']['exchanges']

        # Place Order
        try:
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": "SBIN-EQ",
                "symboltoken": "3045",
                "transactiontype": "BUY",
                "exchange": "NSE",
                "ordertype": "LIMIT",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": "19500",
                "squareoff": "0",
                "stoploss": "0",
                "quantity": "1"
            }
            orderid = smartApi.placeOrder(orderparams)
            logger.info(f"PlaceOrder : {orderid}")
        except Exception as e:
            logger.exception(f"Order placement failed: {e}")

# WebSocket Setup
from SmartApi.smartWebSocketV2 import SmartWebSocketV2

def websocket_example():
    try:
        token = "XX2N5KOLPKRYYWQI2EZ7WANUIM"
        totp = pyotp.TOTP(token).now()  # Generate TOTP here too
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    # Now use the valid totp for generating the session
    authToken = smartApi.generateSession(username, pwd, totp)['data']['jwtToken']
    feedToken = smartApi.getfeedToken()

    API_KEY = 'dzZ33rQv'
    CLIENT_CODE = 'R306312'
    correlation_id = "abc123"
    mode = 1

    token_list = [{"exchangeType": 1, "tokens": ["26009"]}]

    sws = SmartWebSocketV2(authToken, API_KEY, CLIENT_CODE, feedToken)

    def on_data(wsapp, message):
        logger.info("Ticks: {}".format(message))

    def on_open(wsapp):
        logger.info("on open")
        sws.subscribe(correlation_id, mode, token_list)

    def on_error(wsapp, error):
        logger.error(error)

    def on_close(wsapp):
        logger.info("Close")

    # Assign the callbacks
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    sws.connect()

# Running the functions
if __name__ == "__main__":
    generate_session_and_place_order()
    websocket_example()
