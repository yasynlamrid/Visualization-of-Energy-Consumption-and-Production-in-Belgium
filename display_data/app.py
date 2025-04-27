from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client['energy_data']

consumption_collection = db['energy_data_consumption']
flow_collection = db['flow_table_total']
production_collection = db['production_table_total']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_date = request.form.get('date')


        consumption_data = list(consumption_collection.find({'date': selected_date},
                                                            {'_id': 0, 'date': 1, 'time': 1, 'mostrecentforecast': 1}))
        flow_data = list(flow_collection.find({'date': selected_date},
                                              {'_id': 0, 'date': 1, 'time': 1, 'physicalflowatborder_total': 1}))
        production_data = list(production_collection.find({'date': selected_date}, {'_id': 0, 'date': 1, 'time': 1,
                                                                                    'dayaheadgenerationschedule_total': 1}))


        merged_data = {}
        for data in consumption_data:
            key = (data['date'], data['time'])
            merged_data[key] = {'date': data['date'], 'time': data['time'],
                                'mostrecentforecast': data['mostrecentforecast'],
                                'physicalflowatborder_total': 0}  # Initialisez à 0

        for data in flow_data:
            key = (data['date'], data['time'])
            if key in merged_data:
                merged_data[key]['physicalflowatborder_total'] = data['physicalflowatborder_total']

        for data in production_data:
            key = (data['date'], data['time'])
            if key in merged_data:
                merged_data[key]['dayaheadgenerationschedule_total'] = data['dayaheadgenerationschedule_total']


        for key, data in merged_data.items():
            data['calculated_column'] = (
                    data.get('dayaheadgenerationschedule_total', 0)
                    - data.get('mostrecentforecast', 0)
                    + data.get('physicalflowatborder_total', 0)
            )


        data_for_display = list(merged_data.values())

        return render_template('tables_view.html', data=data_for_display, selected_date=selected_date)
    else:

        return render_template('tables_view.html')



if __name__ == '__main__':
    app.run(debug=True)
