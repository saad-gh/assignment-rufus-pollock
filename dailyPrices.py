import pandas as pd
import csv
import datetime
import os.path


class DailyPrices:

    def __init__(self):
        self.std_strftime = "%Y-%m-%d"
        self.url = "https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls"
        self.df_fresh_dp = pd.read_excel(self.url, sheet_name = 'Data 1')

    def downloadDailyPrices(self):    

        #   Standardizing into a string format
        self.df_fresh_dp['Back to Contents'] = self.df_fresh_dp['Back to Contents'].apply(
            lambda x: x.strftime(self.std_strftime) if isinstance(x, datetime.datetime) else x )

        dates = self.df_fresh_dp['Back to Contents'].values  # Read dates column    
        prices = self.df_fresh_dp['Data 1: Henry Hub Natural Gas Spot Price (Dollars per Million Btu)'].values  # Read prices column
        
        # removing unrequired data
        dates = dates[1:]
        prices = prices[1:]

        # Setting standardized headers
        dates[0] = "dates"
        prices[0] = "prices"

        rows = zip(dates,prices)
        
        if not os.path.exists("dailyPrices.csv"):
            with open("dailyPrices.csv", "w",newline='') as dp: 
                    writer = csv.writer(dp)
                    for row in rows:                                        
                        writer.writerow(row)
        return 1

    def updateDailyPrices(self):

        dates = self.df_fresh_dp['Back to Contents'].values  # Read dates column
        latest_date = dates[-1].strftime(self.std_strftime)  # Extract latest date and standardize into string format
        prices = self.df_fresh_dp['Data 1: Henry Hub Natural Gas Spot Price (Dollars per Million Btu)'].values  # Read prices column
        latest_price = prices[-1] # Extract latest price
        
        df_old_dp = pd.read_csv("dailyPrices.csv")

        if df_old_dp['dates'].values[-1] == latest_date and df_old_dp['prices'].values[-1] == latest_price:
            return 0
        else:
            latest_row = [latest_date,latest_price]

        with open("dailyPrices.csv", "a",newline='') as dp: 
                writer = csv.writer(dp)                       
                writer.writerow(latest_row)
        return 1