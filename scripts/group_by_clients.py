import pandas as pd


def group_by_clients(df):
    clients = [
        df.groupby("id_client").get_group(i).copy() for i in df["id_client"].unique()
    ]

    # pour qu'on puisse traiter les jours facilements on change un peu le format :
    """
    reference_date = pd.to_datetime("2021-01-01")
    for i in range(len(clients)):
        clients[i]["jour"] = clients[i]["horodate"].map(
            lambda x: (x - reference_date).days
        )
    """
    return clients
