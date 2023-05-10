import pandas as pd
from sklearn.linear_model import LinearRegression
from metrics import metrics


def creation_model(df, xarg, yarg):
    n = df["id_client"].max()
    # train_size = int(len(df.groupby("id_client").get_group(1)) * 0.8)
    # date_lim = df.groupby("id_client").get_group(1)["horodate"][:train_size].iloc[-1]
    train = df[df["horodate"] <= pd.to_datetime("2022-08-31")]
    test = df[df["horodate"] > pd.to_datetime("2022-08-31")]
    X_train = train.copy()[xarg]
    Y_train = train.copy()[yarg]
    X_test = test.copy()[xarg]
    Y_test = test.copy()[yarg]

    # création du model
    model = LinearRegression()
    model.fit(X_train, Y_train)
    y_pred = model.predict(X_test)

    comp = pd.DataFrame(Y_test.copy())
    comp["pred"] = y_pred
    comp["id_client"] = X_test["id_client"]
    evaluation_model = []

    evaluation_model = []
    for i in range(n):
        y = comp.groupby("id_client").get_group(i + 1)["pred"]
        y2 = comp.groupby("id_client").get_group(i + 1)["real_consumption"]
        evaluation_model.append(metrics(y2, y))
    return evaluation_model
