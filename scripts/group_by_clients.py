import pandas as pd


def group_by_clients(df):
    clients = [
        df.groupby("id_client").get_group(i).copy() for i in df["id_client"].unique()
    ]
    return clients
