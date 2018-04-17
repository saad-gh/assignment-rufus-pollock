import pandas as pd
import csv

def updateDailyPrices():
    url = "https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls"

    df_fresh_dp = pd.read_excel(url, sheet_name = 'Data 1')

    dates = df_fresh_dp['Back to Contents'].values  # Read dates column
    latest_date = dates[-1]  # Extract latest date
    prices = df_fresh_dp['Data 1: Henry Hub Natural Gas Spot Price (Dollars per Million Btu)'].values  # Read prices column
    latest_price = prices[-1] # Extract latest price

    df_old_dp = pd.read_csv("dailyPrices.csv")

    # print(df_old_dp['Year'].values[-1], ' L ', df_old_dp['Price'].values[-1])

    if df_old_dp['Year'].values[-1] == latest_date.strftime("%Y-%m-%d %H:%M:%S") and df_old_dp['Price'].values[-1] == latest_price:
        return 0
    else:
        latest_row = [latest_date,latest_price]

    with open("dailyPrices.csv", "a") as dp: 
            writer = csv.writer(dp)            
            writer.writerow(latest_row)
    return 1

updateDailyPrices()