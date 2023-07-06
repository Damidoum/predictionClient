import pandas as pd


def import_data(path="../"):
    # on commence par lire la table
    df = pd.read_csv(path + "data/complete_merged_dataset.csv", sep=";")
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


def set_up_index(index):
    index.rename({"Date": "horodate"}, axis=1, inplace=True)
    index["horodate"] = pd.to_datetime(index["horodate"])
    index.set_index("horodate", inplace=True)
    index = index.asfreq("D")
    index.reset_index(inplace=True)
    index = index.fillna(method="ffill")
    date = (index["horodate"] >= pd.to_datetime("2021-01-01")) & (
        index["horodate"] <= pd.to_datetime("2023-01-31")
    )
    index = index[date]
    index.reset_index(inplace=True)
    index = index[["horodate", "Open"]]
    return index


def import_data_complete(path="../"):
    data = import_data(path)
    CAC = pd.read_csv(path + "data/^FCHI.csv")
    AEX = pd.read_csv(path + "data/^AEX.csv")
    BFX = pd.read_csv(path + "data/^BFX.csv")
    STOXX = pd.read_csv(path + "data/^STOXX50E.csv")
    Airliquide = pd.read_csv(path + "data/AI.PA.csv")
    gasNat = pd.read_csv(path + "data/gasNat.csv").rename({"Ouvert": "Open"}, axis=1)

    CAC = set_up_index(CAC)
    AEX = set_up_index(AEX)
    BFX = set_up_index(BFX)
    STOXX = set_up_index(STOXX)
    Airliquide = set_up_index(Airliquide)
    gasNat = set_up_index(gasNat)

    CAC.rename({"Open": "CAC"}, axis=1, inplace=True)
    AEX.rename({"Open": "AEX"}, axis=1, inplace=True)
    BFX.rename({"Open": "BFX"}, axis=1, inplace=True)
    STOXX.rename({"Open": "STOXX"}, axis=1, inplace=True)
    Airliquide.rename({"Open": "Airliquide"}, axis=1, inplace=True)
    gasNat.rename({"Open": "gasNat"}, axis=1, inplace=True)

    # CAC.rename({"Volume": "CAC"}, axis = 1, inplace = True)
    # AEX.rename({"Volume": "AEX"}, axis = 1, inplace = True)
    # BFX.rename({"Volume": "BFX"}, axis = 1, inplace = True)
    # STOXX.rename({"Volume": "STOXX"}, axis = 1, inplace = True)

    # il faut merge avec le tableau principal
    data = pd.merge(data, CAC, on=["horodate"], how="left")
    data = pd.merge(data, AEX, on=["horodate"], how="left")
    data = pd.merge(data, BFX, on=["horodate"], how="left")
    data = pd.merge(data, STOXX, on=["horodate"], how="left")
    data = pd.merge(data, Airliquide, on=["horodate"], how="left")
    data = pd.merge(data, gasNat, on=["horodate"], how="left")

    # on retire quelques clients problématiques
    data = data[~(data["id_client"].isin([8, 9, 17, 23, 28, 37, 38, 49]))]
    return data
