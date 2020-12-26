import datetime
from kite_basics import KiteConnectFunctions
from strategy_collection import SimpleMovingAverageCrossover
from strategy_collection import TwoMovingAverageCrossover
import time
import re


if __name__ == "__main__":
    
    FIRSTWINDOW = 9
    SECONDWINDOW = 21
    DELTA_HYST_TIME = 3
    
    kiteFunc = KiteConnectFunctions()
    mva_9_21_cross = TwoMovingAverageCrossover(FIRSTWINDOW,SECONDWINDOW,DELTA_HYST_TIME)
    
    # Instrument token of RELIANCE
    instrument_name = "RELIANCE"
    instrument_token = "738561" 
    # Interval(minute, day, 3 minute, 5 minute...)
    interval = "5minute"

    try:
        value_interval,type_interval = [re.findall(r'(\d+)(\w+)', interval)[0]][0]
    except:
        type_interval = "minute"
        value_interval = 5    
    
    if not type_interval in ['minute','second']:
        type_interval = "minute"
        value_interval = 5

    while(1):
        now = datetime.datetime.now()
        delta = datetime.timedelta(minutes = value_interval*(SECONDWINDOW+DELTA_HYST_TIME+2))
        #delta = dt.timedelta(eval(type_interval+'s') = value_interval*(21+5))
        from_date = now - delta
        from_date_str = from_date.strftime('%Y-%m-%d %H:%M:%S')
        to_date_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        recorded_data = kiteFunc.get_history_data(instrument_token,from_date_str,to_date_str,interval)
        decision_taken,price_for_decision = mva_9_21_cross.run_strategy(recorded_data)
        print("Placing {0} type of order at price {1}".format(decision_taken,price_for_decision))
        if decision_taken is not None:
            kiteFunc.place_order(instrument_name,decision_taken,exchange_name = 'NSE',no_of_quantity = 1,order_type = "MARKET",product="CNC")
        if type_interval == 'minute':
            time.sleep(value_interval*60)
        elif type_interval == 'second':
            time.sleep(value_interval)
        else:
            raise ValueError('Not implemented for this interval setting.')
