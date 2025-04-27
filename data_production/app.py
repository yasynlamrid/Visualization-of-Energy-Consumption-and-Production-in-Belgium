from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from data_fetcher import fetch_data_for_date
from data_storer import insert_sorted_data_to_mongodb, store_total_data

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")

db = client["energy_data"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date_input = request.form['date_input']
        return redirect(url_for('show_data', date=date_input))
    return render_template('index.html')

@app.route('/show_data/<date>', methods=['GET'])
def show_data(date):
    data_for_mongodb, total_data_by_time = fetch_data_for_date(date)

    for fuel_code, data in data_for_mongodb.items():
        collection_name = f"table_{fuel_code}"
        insert_sorted_data_to_mongodb(client, collection_name, data)

    store_total_data(client, total_data_by_time, date)

    collection = db["production_table_total"]
    data = collection.find({'date': date})
    data_list = list(data)
    return render_template('data.html', data=data_list, date=date)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)