import csv
from dailyPrices import DailyPrices
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main.html")

def csv_reader(file_obj):    
    # Read a csv file    
    reader = csv.reader(file_obj)
    
    # iterate over the header
    i = iter(reader)
    next(i)

    return jsonify([{"date":row[0],"price":row[1]} for row in reader if len(row)])

@app.route('/dailyPrices', methods=['GET'])
def getDailyPrices():
    # update csv
    dp = DailyPrices()
    dp.updateDailyPrices()

    csv_path = "data\\dailyPrices.csv"
    with open(csv_path, "rt") as f_obj:
        return csv_reader(f_obj)

if __name__ == '__main__':
    app.run(debug=True)

# References:
# https://dzone.com/articles/python-101-reading-and-writing
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# https://bl.ocks.org/mbostock/3883245
# http://d3indepth.com/scales/#scales-with-continuous-input-and-continuous-output