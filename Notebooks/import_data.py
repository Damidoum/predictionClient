import pandas as pd


def import_data():
    # on commence par lire la table
    df_global = pd.read_csv("../data/complete_merged_dataset.csv", sep=";")

    # sur chaque date la fin n'est pas indispensable car l'heure est toujours la même, on peut donc enlever cette partie pour simplifier.
    parser = lambda x: x[:-21]
    df_global["horodate"] = df_global["horodate"].map(parser)

    # puis on peut utiliser un type spécialisé dans le traitement des dates :
    df_global["horodate"] = pd.to_datetime(df_global["horodate"])

    # dans un premier temps les colonnes dq et top ne nous intéressent pas :
    del df_global["dq"]
    del df_global["top"]

    # on rename la colonne percentile_50
    df_global = df_global.rename(columns={"percentile_50": "prediction"})

    # de plus on aimerait que les id_client se suivent, par exemple 8 n'est pas présent.
    id_client = df_global["id_client"].unique()
    id_rename = {}
    for i in range(len(id_client)):
        id_rename[str(id_client[i])] = i + 1
    client_rename = lambda x: id_rename[str(x)]
    df_global["id_client"] = df_global["id_client"].map(client_rename)

    return df_global
