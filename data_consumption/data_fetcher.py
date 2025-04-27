import requests
from dateutil.parser import parse

def fetch_data_for_date(date_input):
    data_for_mongodb = []
    base_url = "https://opendata.elia.be"
    url = f"{base_url}/api/explore/v2.1/catalog/datasets/ods001/records?limit=100&refine=datetime%3A%22{date_input}%22"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            results = data['results']
            data_for_mongodb=[]
            for result in results:
                datetime_obj = parse(result['datetime'])
                date_str = datetime_obj.strftime('%Y-%m-%d')
                time_str = datetime_obj.strftime('%H:%M')
                schedule_value = result['mostrecentforecast']
                data_for_mongodb.append({
                    'date': date_str,
                    'time': time_str,
                    'mostrecentforecast': schedule_value,
                })

        else:
            print(f"La clé 'results' n'est pas présente dans les données retournées par l'API pour le carburant.")
    else:
        print(f"Échec de la requête API pour le carburant. Statut : {response.status_code}")
    print(schedule_value)
    return data_for_mongodb



