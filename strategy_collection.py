import pdb

class SimpleMovingAverageCrossover:

    def __init__(self):
        self.total_closing_price = 0
        self.last_order_placed = None
        self.last_order_price = 0
        self.profit = 0

    def run_strategy(self,recorded_data):
        record_count = 0
        for record in recorded_data:
            record_count += 1
            self.total_closing_price += record["close"]
            
            #Moving avearge is calculated for every 5 ticks(recorded_data)
            if record_count >= 5:
                moving_average = self.total_closing_price/5

                # If moving average is greater than last tick, place a buy order
                if record["close"] > moving_average:
                    if self.last_order_placed == "SELL" or self.last_order_placed is None:
                        
                        # If last order was sell, exit the stock first
                        if self.last_order_placed == "SELL":
                            print("Exit SELL")

                            # Calculate profit
                            self.profit += self.last_order_price - record["close"]
                            self.last_order_price = record["close"]

                        # Fresh BUY order
                        print("place new BUY order")
                        self.last_order_placed = "BUY"

                # If moving average is lesser than last tick, and there is a position, place a sell order
                elif record["close"] < moving_average:
                    if self.last_order_placed == "BUY":
                        
                        # As last order was a buy, first let's exit the position
                        print("Exit BUY")
                        
                        # Calculate profit
                        self.profit += record["close"] - self.last_order_price
                        self.last_order_price = record["close"]
                        
                        # Fresh SELL order
                        print("place new SELL order")
                        self.last_order_placed = "SELL"
                self.total_closing_price -= recorded_data[record_count-5]["close"]
        print("Gross Profit ", self.profit)
        # PLace the last order 
        return self.last_order_placed,self.last_order_price



class TwoMovingAverageCrossover:

    def __init__(self,first_window = 9,second_window=21,delta_hyst_time = 3):
        self.FIRST_WINDOW = first_window
        self.SECOND_WINDOW = second_window
        self.DELTA_HIST_TIME = delta_hyst_time
        self.last_x_closing_price = 0
        self.last_y_closing_price = 0
        self.last_order_placed = None
        self.last_order_price = 0
        self.profit = 0
        self.cross_x_on_y_time = 0
        self.cross_y_on_x_time = 0
    
    def run_strategy(self,recorded_data):
        self.cross_x_on_y_time = 0
        self.cross_y_on_x_time = 0
        record_count = 0

        #for record in recorded_data:
        for i in range(0,len(recorded_data)):
            record = recorded_data.iloc[i]
            record_count += 1

            self.last_x_closing_price += record["close"]
            self.last_y_closing_price += record["close"]
            
            if record_count >= max(self.FIRST_WINDOW,self.SECOND_WINDOW):
                moving_average_x = self.last_x_closing_price/self.FIRST_WINDOW
                moving_average_y = self.last_y_closing_price/self.SECOND_WINDOW
                
                if (moving_average_x >= moving_average_y):
                    self.cross_y_on_x_time = 0
                    if(self.cross_x_on_y_time <= 1):
                        delta_hyst_value = 0.001 * record["close"]
                    self.cross_x_on_y_time += 1
                    if((moving_average_x > moving_average_y + delta_hyst_value) and (self.cross_x_on_y_time > self.DELTA_HIST_TIME)):
                        if self.last_order_placed == "SELL" or self.last_order_placed is None:
                            # If last order was sell, exit the stock first
                            if self.last_order_placed == "SELL":
                                print("Exit SELL")
                                # Calculate profit
                                self.profit += self.last_order_price - record["close"]
                                self.last_order_price = record["close"]
                            # Fresh BUY order
                            print("place new BUY order")
                            self.last_order_placed = "BUY"
                    else:
                        print("Wait for Confirmation of trend up")
                else:
                    self.cross_x_on_y_time = 0
                    if(self.cross_y_on_x_time <= 1):
                        delta_hyst_value = 0.001 * record["close"]
                    self.cross_y_on_x_time += 1
                    if((moving_average_x < moving_average_y - delta_hyst_value) and (self.cross_y_on_x_time > self.DELTA_HIST_TIME)):
                        if self.last_order_placed == "BUY":
                            
                            # As last order was a buy, first let's exit the position
                            print("Exit BUY")
                            
                            # Calculate profit
                            self.profit += record["close"] - self.last_order_price
                            self.last_order_price = record["close"]
                            
                            # Fresh SELL order
                            print("place new SELL order")
                            self.last_order_placed = "SELL"
                    else:
                        print("Wating for down trend confirmation")

            if(record_count >= self.FIRST_WINDOW):
                self.last_x_closing_price -= recorded_data.iloc[record_count-self.FIRST_WINDOW]["close"]
                #self.last_x_closing_price -= recorded_data[record_count-self.FIRST_WINDOW]["close"]
            if(record_count >= self.SECOND_WINDOW):
                self.last_y_closing_price -= recorded_data.iloc[record_count-self.SECOND_WINDOW]["close"]
                #self.last_y_closing_price -= recorded_data[record_count-self.SECOND_WINDOW]["close"]

        print("Gross Profit ", self.profit)
        # PLace the last order 
        return self.last_order_placed,self.last_order_price
        