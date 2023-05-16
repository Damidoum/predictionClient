from typing import List, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# librairies perso
from group_by_clients import group_by_clients
from metrics import metrics


def make_train_test_set(
    clients: List, x_vars: List[str], y_vars: List[str], lim_date: float
) -> Tuple[List, List, List, List]:
    train_size = int(len(clients[0]) * lim_date)
    train_data = [client[:train_size] for client in clients]
    test_data = [client[train_size:] for client in clients]

    # on garde ensuite que les x_vars et y_vars choisis
    X_train = [train_client[x_vars] for train_client in train_data]
    y_train = [train_client[y_vars] for train_client in train_data]

    X_test = [test_client[x_vars] for test_client in test_data]
    y_test = [test_client[y_vars] for test_client in test_data]

    return X_train, X_test, y_train, y_test, test_data


def creation_model(df, xargs, yargs, lim_date, random_forest=False, n_estimators=150):
    n = df["id_client"].max()
    train_size = int(len(df.groupby("id_client").get_group(1)) * lim_date)
    date_lim = df.groupby("id_client").get_group(1)["horodate"][:train_size].iloc[-1]
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
        y2 = comp.groupby("id_client").get_group(i)["real_consumption"]
        evaluation_model.append(metrics(y2, y))
    return model, evaluation_model


def creation_model_by_client(
    df, xargs, yargs, lim_date, random_forest=False, n_estimators=150
):
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
        evaluation_model.append(metrics(y_test[i], y_pred[i]))

    return models, evaluation_model


def complet_process(
    df, xargs, yargs, lim_date, group=False, random_forest=False, n_estimators=150
):
    if group:
        model, eval_model = creation_model_by_client(
            df, xargs, yargs, lim_date, random_forest, n_estimators
        )
    else:
        model, eval_model = creation_model(
            df, xargs, yargs, lim_date, random_forest, n_estimators
        )
    return model, eval_model
