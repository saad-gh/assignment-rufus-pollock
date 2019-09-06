import pandas as pd
import csv
import datetime
import os.path


class Prices:

    def __init__(self,url,period):
        self.std_strftime = "%Y-%m-%d"
        self.url = url
        self.fresh_prices = pd.read_excel(self.url, sheet_name = 'Data 1')
        self.path_dp = "data/" + period + ".csv"

        if period == "weekly":
            self.prices_column_key = "Data 1: Weekly Henry Hub Natural Gas Spot Price (Dollars per Million Btu)"
        else:
            self.prices_column_key = "Data 1: Henry Hub Natural Gas Spot Price (Dollars per Million Btu)"

    def download_prices(self):    
        #   Standardizing into a string format
        self.fresh_prices['Back to Contents'] = self.fresh_prices['Back to Contents'].apply(
            lambda x: x.strftime(self.std_strftime) if isinstance(x, datetime.datetime) else x )

        dates = self.fresh_prices['Back to Contents'].values  # Read dates column    
        prices = self.fresh_prices[self.prices_column_key].values  # Read prices column
        
        # removing unrequired data
        dates = dates[1:]
        prices = prices[1:]

        # Setting standardized headers
        dates[0] = "dates"
        prices[0] = "prices"

        rows = zip(dates,prices)        
        
        with open(self.path_dp, "w",newline='') as dp: 
                    writer = csv.writer(dp)
                    for row in rows:                                        
                        writer.writerow(row)

    def update_prices(self):
        if os.path.exists(self.path_dp):
            old_prices = pd.read_csv(self.path_dp)
        else:
            self.download_prices()
            return 1

        dates = self.fresh_prices['Back to Contents'].values  # Read dates column
        latest_date = dates[-1].strftime(self.std_strftime)  # Extract latest date and standardize into string format
        prices = self.fresh_prices[self.prices_column_key].values  # Read prices column
        latest_price = prices[-1] # Extract latest price        

        if old_prices['dates'].values[-1] == latest_date and old_prices['prices'].values[-1] == latest_price:
            return 0
        else:
            latest_row = [latest_date,latest_price]

        with open(self.path_dp, "a",newline='') as dp: 
            writer = csv.writer(dp)                       
            writer.writerow(latest_row)

if __name__ == "__main__":
    dp = Prices("https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls","daily")
    wp = Prices("https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDw.xls","weekly")
    mp = Prices("https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls","monthly")
    ap = Prices("https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDa.xls","annual")
   
    dp.update_prices()
    wp.update_prices()
    mp.update_prices()
    ap.update_prices()