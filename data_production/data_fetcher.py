import requests
from dateutil.parser import parse


categories = ["CP", "LF", "NG", "NU", "Other", "WA", "WI"]

def fetch_data_for_date(date_input):
    total_data_by_time = {}
    data_for_mongodb = {}

    for fuel_code in categories:
        api_url = f"https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods034/records?limit=100&refine=fuelcode%3A%22{fuel_code}%22&refine=datetime%3A%22{date_input}%22"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                results = data['results']
                mongodb_data = []
                for result in results:
                    datetime_obj = parse(result['datetime'])
                    date_str = datetime_obj.strftime('%Y-%m-%d')
                    time_str = datetime_obj.strftime('%H:%M')
                    schedule_value = result['dayaheadgenerationschedule']

                    mongodb_data.append({
                        'date': date_str,
                        'time': time_str,
                        'dayaheadgenerationschedule': schedule_value,
                        'fuel_code': fuel_code
                    })

                    if time_str not in total_data_by_time:
                        total_data_by_time[time_str] = schedule_value
                    else:
                        total_data_by_time[time_str] += schedule_value

                data_for_mongodb[fuel_code] = mongodb_data
            else:
                print(f"La clé 'results' n'est pas présente dans les données retournées par l'API pour le carburant {fuel_code}.")
        else:
            print(f"Échec de la requête API pour le carburant {fuel_code}. Statut : {response.status_code}")

    return data_for_mongodb, total_data_by_time
