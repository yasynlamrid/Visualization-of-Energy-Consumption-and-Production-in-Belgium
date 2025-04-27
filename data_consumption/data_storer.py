def insert_sorted_data_to_mongodb(client, collection_name, data):
    try:
        db = client["energy_data"]
        collection = db[collection_name]

        if data:
            sorted_data = sorted(data, key=lambda x: x['time'])
            result = collection.insert_many(sorted_data)
            print(f"Données triées et insérées pour la collection {collection.name}. Nombre de documents insérés : {len(result.inserted_ids)}")
        else:
            print(f"Aucune nouvelle donnée à insérer pour la collection {collection.name}.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'insertion des données : {e}")
