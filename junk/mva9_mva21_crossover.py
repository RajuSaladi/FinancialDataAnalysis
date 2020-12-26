from kiteconnect import KiteConnect 

# Initialize all the variables we need
api_key = "YOUR API KEY"
access_token = "YOUR ACCESS TOKEN"
client_id = "YOUR CLIENT ID"

# Instrument token of RELIANCE
instrument_token = "738561" 

# Dates between which we need historical data
from_date = "2016-10-01"
to_date = "2016-10-17"

# Interval(minute, day, 3 minute, 5 minute...)
interval = "5minute"

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Gets historical data from Kite Connect
def get_historical_data():
	return kite.historical(instrument_token, from_date, to_date, interval)

"""
	 Implementation of the moving average strategy.
	 We go through the historical records that 
	 we received form Kite Connect, calculate moving average,
	 and place a BUY or SELL order.
"""
def strategy(records):
    FIRST_WINDOW = 9
    SECOND_WINDOW = 21
    DELTA_HIST_TIME = 3
	last_x_closing_price = 0
	last_y_closing_price = 0
	record_count = 0
	order_placed = False
	last_order_placed = None
	last_order_price = 0
	profit = 0
    
    cross_x_on_y_time = 0
    cross_y_on_x_time = 0
    
	for record in records:
		record_count += 1

        last_x_closing_price += record["close"]
        last_y_closing_price += record["close"]
		
		if record_count >= max(FIRST_WINDOW,SECOND_WINDOW):
			moving_average_x = last_x_closing_price/FIRST_WINDOW
			moving_average_y = last_y_closing_price/SECOND_WINDOW
            
            if (moving_average_x >= moving_average_y):
                cross_x_on_y_time += 1
                if(cross_x_on_y_time <= 1):
                    delta_hyst_value = 0.001 * record["close"]
                if(moving_average_x > moving_average_y + delta_hyst_value) and (cross_x_on_y_time > DELTA_HIST_TIME)):
                    if last_order_placed == "SELL" or last_order_placed is None:
                        # If last order was sell, exit the stock first
                        if last_order_placed == "SELL":
                            print "Exit SELL"
                            # Calculate profit
                            profit += last_order_price - record["close"]
                            last_order_price = record["close"]
                        # Fresh BUY order
                        print "place new BUY order"
                        last_order_placed = "BUY"
                else:
                    print("Wait for Confirmation of trend up")
                   
            else:
                cross_x_on_y_time = 0
                
                if(moving_average_x < moving_average_y):
                    cross_y_on_x_time += 1
                    if(cross_y_on_x_time <= 1):
                        delta_hyst_value = 0.001 * record["close"]
                    if(moving_average_x < moving_average_y - delta_hyst_value) and (cross_y_on_x_time > DELTA_HIST_TIME)):
                        if last_order_placed == "BUY":
                            
                            # As last order was a buy, first let's exit the position
                            print "Exit BUY"
                            
                            # Calculate profit
                            profit += record["close"] - last_order_price
                            last_order_price = record["close"]
                            
                            # Fresh SELL order
                            print "place new SELL order"
                            last_order_placed = "SELL"
                    else:
                        print("Wating for down trend confirmation")

		if(record_count >= FIRST_WINDOW):
			last_x_closing_price -= records[record_count-FIRST_WINDOW]["close"]
        if(record_count >= SECOND_WINDOW):
			last_y_closing_price -= records[record_count-SECOND_WINDOW]["close"]

	print "Gross Profit ", profit
	# PLace the last order 
	place_order(last_order_placed)

# Place an order based upon transaction type(BUY/SELL)
def place_order(transaction_type):
	kite.order_place(tradingsymbol="RELIANCE", exchange="NSE", quantity=1, transaction_type=transaction_type, order_type="MARKET", product="CNC")


def start():
	records = get_historical_data()
	strategy(records)

start()