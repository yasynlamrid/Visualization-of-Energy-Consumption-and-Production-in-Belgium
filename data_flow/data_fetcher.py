import requests
from dateutil.parser import parse

countries = ["France", "Luxembourg", "UnitedKingdom", "Netherlands", "Germany"]

def fetch_data_for_date(date_input):
    total_data_by_time = {}
    data_for_mongodb = {}

    for country in countries:
        base_url = "https://opendata.elia.be"
        api_url = f"{base_url}/api/explore/v2.1/catalog/datasets/ods026/records?limit=100&refine=controlarea%3A{country}&refine=datetime%3A{date_input}"
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
                    schedule_value = result['physicalflowatborder']

                    mongodb_data.append({
                        'date': date_str,
                        'time': time_str,
                        'physicalflowatborder': schedule_value,
                        'country': country
                    })

                    if time_str not in total_data_by_time:
                        total_data_by_time[time_str] = schedule_value
                    else:
                        total_data_by_time[time_str] += schedule_value

                data_for_mongodb[country] = mongodb_data
            else:
                print(f"La clé 'results' n'est pas présente dans les données retournées par l'API pour le carburant {country}.")
        else:
            print(f"Échec de la requête API pour le carburant {country}. Statut : {response.status_code}")

    return data_for_mongodb, total_data_by_time
