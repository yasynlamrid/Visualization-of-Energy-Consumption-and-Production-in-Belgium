def insert_sorted_data_to_mongodb(client, collection_name, data):
    db = client["energy_data"]
    collection = db[collection_name]

    if data:
        sorted_data = sorted(data, key=lambda x: x['time'])
        collection.insert_many(sorted_data)
        print(f"Données triées et insérées pour la collection {collection.name}.")
    else:
        print(f"Aucune nouvelle donnée à insérer pour la collection {collection.name}.")

def store_total_data(client, total_data_by_time, date_input):
    db = client["energy_data"]
    table_total_collection = db["flow_table_total"]

    for time, total in sorted(total_data_by_time.items()):
        table_total_collection.update_one(
            {'time': time},
            {'$set': {'physicalflowatborder_total': total, 'date': date_input}},
            upsert=True
        )
    print("Mise à jour de table_total terminée.")
