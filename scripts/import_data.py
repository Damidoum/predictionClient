import pandas as pd


def import_data():
    # on commence par lire la table
    df = pd.read_csv("../data/complete_merged_dataset.csv", sep=";")
    df.drop(df[df["id_client"] == 16].index, inplace=True)

    # sur chaque date la fin n'est pas indispensable car l'heure est toujours la même, on peut donc enlever cette partie pour simplifier.
    parser = lambda x: x[:-21]
    df["horodate"] = df["horodate"].map(parser)

    # puis on peut utiliser un type spécialisé dans le traitement des dates :
    df["horodate"] = pd.to_datetime(df["horodate"])

    # dans un premier temps les colonnes dq et top ne nous intéressent pas :
    del df["dq"]
    del df["top"]

    # on rename la colonne percentile_50
    df = df.rename(columns={"percentile_50": "prediction"})

    # de plus on aimerait que les id_client se suivent, par exemple 8 n'est pas présent.
    id_client = df["id_client"].unique()
    id_rename = {}
    for i in range(len(id_client)):
        id_rename[str(id_client[i])] = i + 1
    client_rename = lambda x: id_rename[str(x)]
    df["id_client"] = df["id_client"].map(client_rename)

    return df
