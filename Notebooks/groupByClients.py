import pandas as pd


def group_by_clients(df):
    num_client = df["id_client"].unique()
    clients = [df.groupby("id_client").get_group(i).copy() for i in num_client]

    # pour qu'on puisse traiter les jours facilements on change un peu le format :
    reference_date = pd.to_datetime("2021-01-01")
    for i in num_client:
        clients[i]["jour"] = clients[i]["horodate"].map(
            lambda x: (x - reference_date).days
        )
    return clients
