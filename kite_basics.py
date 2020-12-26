from kiteconnect import KiteConnect 

class KiteConnectFunctions:
	
	def __init__(self):
		# Initialize all the variables we need
        api_key = "YOUR API KEY"
        access_token = "YOUR ACCESS TOKEN"
        client_id = "YOUR CLIENT ID"
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)
        
        # Redirect the user to the login url obtained
        # from kite.login_url(), and receive the request_token
        # from the registered redirect url after the login flow.
        # Once you have the request_token, obtain the access_token
        # as follows.

        #data = kite.generate_session("request_token_here", api_secret="your_secret")
        #self.kite.set_access_token(data["access_token"])
        
    def get_history_data(self,instrument_token,from_date,to_date,interval):
        return kite.historical(instrument_token, from_date, to_date, interval)
    
    def place_order(self,instrument_name,transaction_type,exchange_name = 'NSE',no_of_quantity = 1,order_type = "MARKET",product="CNC"):
        return kite.order_place(tradingsymbol=instrument_name, exchange=exchange_name, quantity=no_of_quantity, transaction_type=transaction_type, order_type=order_type, product=product)
