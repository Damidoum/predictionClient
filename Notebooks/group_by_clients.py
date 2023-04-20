import pandas as pd


def group_by_clients(df_global):
    n = df_global["id_client"].max()
    clients = [
        df_global.groupby("id_client").get_group(i).copy() for i in range(1, n + 1)
    ]

    # pour qu'on puisse traiter les jours facilements on change un peu le format :
    reference_date = pd.to_datetime("2021-01-01")
    for i in range(n):
        clients[i]["jour"] = clients[i]["horodate"].map(
            lambda x: (x - reference_date).days
        )
    return clients
