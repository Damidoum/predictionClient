import pandas as pd
from sklearn.linear_model import LinearRegression
from metrics import metrics
from group_by_clients import group_by_clients
from make_train_test_set import make_train_test_set


def creation_model_by_client(df, xargs, yargs):
    clients = group_by_clients(df)
    n = len(clients)

    X_train, X_test, y_train, y_test, test_data = make_train_test_set(
        clients, xargs, yargs
    )

    models = [LinearRegression() for _ in range(n)]
    for i, model in enumerate(models):
        model.fit(X_train[i], y_train[i])

    y_pred = []
    for i, model in enumerate(models):
        y_pred.append(model.predict(X_test[i]).reshape(len(X_test[i])))

    evaluation_model = []
    for i in range(n):
        evaluation_model.append(metrics(y_test[i], y_pred[i]))

    return evaluation_model
