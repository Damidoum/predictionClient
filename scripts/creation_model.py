from typing import List, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# librairies perso
from group_by_clients import group_by_clients
from metrics import metrics, tab_mesure


def make_train_test_set(
    clients: List, x_vars: List[str], y_vars: List[str], lim_date: float
) -> Tuple[List, List, List, List]:
    """
    description : réalise les ensembles de test / train pour appliquer le modèle de ML
    paramètres :
    - clients : liste contenant un DataFrame par client
    - x_vars : variables à prendre en compte pour l'entrainement
    - y_vars : variables à prédire
    - lim_date : pourcentage des données qu'on veut garder pour l'entrainement
    """
    train_size = int(len(clients[0]) * lim_date)
    train_data = [client[:train_size] for client in clients]
    test_data = [client[train_size:] for client in clients]

    # on garde ensuite que les x_vars et y_vars choisis
    X_train = [train_client[x_vars] for train_client in train_data]
    y_train = [train_client[y_vars] for train_client in train_data]

    X_test = [test_client[x_vars] for test_client in test_data]
    y_test = [test_client[y_vars] for test_client in test_data]

    return X_train, X_test, y_train, y_test, test_data


def creation_model(
    df: pd.DataFrame,
    xargs: List[str],
    yargs: List[str],
    lim_date: float,
    random_forest=False,
    n_estimators=150,
):
    """
    description : crée le modèle à partir des données complètes (en ne groupant pas le DataFrame par client)
    paramètres :
    - df : DataFrame des données complètes
    - x_args : variables à prendre en compte pour l'entrainement
    - y_args : variables à prédire
    -lim_date : pourcentage des données qu'on veut garder pour l'entrainement
    - random_forest : True si on veut utiliser un randomForestRegressor plutôt qu'une LinearRegression
    - n_estimators : paramètre du random forest
    """
    n = df["id_client"].max()
    train_size = int(
        len(df.groupby("id_client").get_group(df["id_client"].unique()[0])) * lim_date
    )
    date_lim = (
        df.groupby("id_client")
        .get_group(df["id_client"].unique()[0])["horodate"][:train_size]
        .iloc[-1]
    )
    train = df[df["horodate"] <= date_lim]
    test = df[df["horodate"] > date_lim]
    X_train = train.copy()[xargs]
    Y_train = train.copy()[yargs]
    X_test = test.copy()[xargs]
    Y_test = test.copy()[yargs]

    # création du model
    if random_forest:
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    else:
        model = LinearRegression()
    model.fit(X_train, np.array(Y_train).ravel())
    y_pred = model.predict(X_test)

    comp = pd.DataFrame(Y_test.copy())
    comp["pred"] = y_pred
    comp["id_client"] = X_test["id_client"]
    evaluation_model = []

    evaluation_model = []
    for i in df["id_client"].unique():
        y = comp.groupby("id_client").get_group(i)["pred"]
        y2 = np.array(comp.groupby("id_client").get_group(i)[yargs]).ravel()
        evaluation_model.append(metrics(y2, y))
    return model, evaluation_model


def creation_model_by_client(
    df: pd.DataFrame,
    xargs: List[str],
    yargs: List[str],
    lim_date: float,
    random_forest=False,
    n_estimators=150,
):
    """
    description : crée le modèle à partir des données complètes (en groupant le DataFrame par client)
    paramètres :
    - df : DataFrame des données complètes
    - x_args : variables à prendre en compte pour l'entrainement
    - y_args : variables à prédire
    -lim_date : pourcentage des données qu'on veut garder pour l'entrainement
    - random_forest : True si on veut utiliser un randomForestRegressor plutôt qu'une LinearRegression
    - n_estimators : paramètre du random forest
    """

    clients = group_by_clients(df)
    n = len(clients)

    X_train, X_test, y_train, y_test, test_data = make_train_test_set(
        clients, xargs, yargs, lim_date
    )

    if random_forest:
        models = [RandomForestRegressor(n_estimators=n_estimators) for _ in range(n)]
    else:
        models = [LinearRegression() for _ in range(n)]

    for i, model in enumerate(models):
        model.fit(X_train[i], np.array(y_train[i]).ravel())

    y_pred = []
    for i, model in enumerate(models):
        y_pred.append(model.predict(X_test[i]).reshape(len(X_test[i])))

    evaluation_model = []
    for i in range(n):
        evaluation_model.append(metrics(np.array(y_test[i]).ravel(), np.array(y_pred[i]).ravel()))

    return models, evaluation_model


def complet_process(
    df: pd.DataFrame,
    xargs: List[str],
    yargs: List[str],
    lim_date: float,
    group=False,
    random_forest=False,
    n_estimators=150,
):
    """
    description : processus complet de création du modèle, on choisit si on veut grouper
    le DataFrame par client ou pas
    paramètres :
    - pd : DataFrame des données complètes
    - x_vars : variables à prendre en compte pour l'entrainement
    - y_vars : variables à prédire
    - lim_date : pourcentage des données qu'on veut garder pour l'entrainement
    - group : True si on veut grouper le DataFrame par client
    - random_forest : True si on veut utiliser un randomForestRegressor plutôt qu'une LinearRegression
    - n_estimators : paramètre du random forest
    """
    if group:
        model, eval_model = creation_model_by_client(
            df, xargs, yargs, lim_date, random_forest, n_estimators
        )
    else:
        model, eval_model = creation_model(
            df, xargs, yargs, lim_date, random_forest, n_estimators
        )
    return model, eval_model


def best_lim_date(
    df: pd.DataFrame,
    xargs: List[str],
    yargs: List[str],
    group=False,
    random_forest=False,
    n_estimators=150,
):

    best_mse = [0,np.inf]
    best_mae = [0, np.inf]
    best_moy = [0, np.inf]
    for i in range(1,90): 
        model, eval_model = complet_process(df, xargs, yargs,i/100, group, random_forest, n_estimators)
        if tab_mesure(eval_model).describe().loc["mean", "MSE"] < best_mse[1] : 
            best_mse[0], best_mse[1] = i/100, tab_mesure(eval_model).describe().loc["mean", "MSE"]
        if tab_mesure(eval_model).describe().loc["mean", "MAE"] < best_mae[1] : 
            best_mae[0], best_mae[1] = i/100, tab_mesure(eval_model).describe().loc["mean", "MAE"]
        if (tab_mesure(eval_model).describe().loc["mean", "MAE"] + tab_mesure(eval_model).describe().loc["mean", "MSE"])/2 < best_moy[1] : 
            best_moy[0], best_moy[1] = i/100, (tab_mesure(eval_model).describe().loc["mean", "MAE"] + tab_mesure(eval_model).describe().loc["mean", "MSE"])/2
    return best_mse[0], best_mae[0], best_moy[0]
        