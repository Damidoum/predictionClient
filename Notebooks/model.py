import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from metrics import metrics


def creation_model(df, xarg, yarg, lim_date, random_forest=False):
    n = df["id_client"].max()
    train_size = int(len(df.groupby("id_client").get_group(1)) * lim_date)
    date_lim = df.groupby("id_client").get_group(1)["horodate"][:train_size].iloc[-1]
    train = df[df["horodate"] <= date_lim]
    test = df[df["horodate"] > date_lim]
    X_train = train.copy()[xarg]
    Y_train = train.copy()[yarg]
    X_test = test.copy()[xarg]
    Y_test = test.copy()[yarg]

    # création du model
    if random_forest:
        model = RandomForestRegressor(n_estimators=150, random_state=42)
    else:
        model = LinearRegression()
    model.fit(X_train, Y_train)
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
