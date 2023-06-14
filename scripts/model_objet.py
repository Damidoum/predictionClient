from typing import List, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor


# librairies perso
from metrics import metrics, tab_mesure
from creation_model import complet_process


class Model:
    def __init__(
        self,
        df,
        xargs,
        yargs,
        lim_date,
        group=False,
        type_regressor="Linear",
    ) -> None:
        self.df = df
        self.xargs = xargs
        self.yargs = yargs
        self.group = group
        self.lim_date = lim_date
        self.type_regressor = type_regressor

    def generate_model(self):
        if not self.group:
            if self.type_regressor == "random_forest":
                self.model = RandomForestRegressor()
            elif self.type_regressor == "gradient_boosting":
                self.model = GradientBoostingRegressor()
            else:
                self.model = LinearRegression()

        else:
            if self.type_regressor == "random_forest":
                self.model = [
                    RandomForestRegressor() for _ in self.df["id_client"].unique()
                ]
            elif self.type_regressor == "gradient_boosting":
                self.model = [
                    GradientBoostingRegressor() for _ in self.df["id_client"].unique()
                ]
            else:
                self.model = [LinearRegression() for _ in self.df["id_client"].unique()]

    def best_lim_date(self):
        best_mse = [0, np.inf]
        best_mae = [0, np.inf]
        best_moy = [0, np.inf]
        for i in range(1, 90):
            model, eval_model = complet_process(
                self.df,
                self.xargs,
                self.yargs,
                i / 100,
                self.group,
                self.random_forest,
                n_estimators=150,
            )
            if tab_mesure(eval_model).describe().loc["mean", "MSE"] < best_mse[1]:
                best_mse[0], best_mse[1] = (
                    i / 100,
                    tab_mesure(eval_model).describe().loc["mean", "MSE"],
                )
            if tab_mesure(eval_model).describe().loc["mean", "MAE"] < best_mae[1]:
                best_mae[0], best_mae[1] = (
                    i / 100,
                    tab_mesure(eval_model).describe().loc["mean", "MAE"],
                )
            if (
                tab_mesure(eval_model).describe().loc["mean", "MAE"]
                + tab_mesure(eval_model).describe().loc["mean", "MSE"]
            ) / 2 < best_moy[1]:
                best_moy[0], best_moy[1] = (
                    i / 100,
                    (
                        tab_mesure(eval_model).describe().loc["mean", "MAE"]
                        + tab_mesure(eval_model).describe().loc["mean", "MSE"]
                    )
                    / 2,
                )
        return best_mse[0], best_mae[0], best_moy[0]

    def generate_train_set(self):
        train_size = int(
            len(
                self.df.groupby("id_client").get_group(self.df["id_client"].unique()[0])
            )
            * self.lim_date
        )
        self.date_lim = (
            self.df.groupby("id_client")
            .get_group(self.df["id_client"].unique()[0])["horodate"][:train_size]
            .iloc[-1]
        )
        if not self.group:
            train = self.df[self.df["horodate"] <= self.date_lim]
            test = self.df[self.df["horodate"] > self.date_lim]
            self.x_train = train.copy()[self.xargs]
            self.y_train = train.copy()[self.yargs]
            self.x_test = test.copy()[self.xargs]
            self.y_test = test.copy()[self.yargs]
        else:
            self.clients = [
                self.df.groupby("id_client").get_group(i).copy()
                for i in self.df["id_client"].unique()
            ]

            train_data = [client[:train_size] for client in self.clients]
            test_data = [client[train_size:] for client in self.clients]

            # on garde ensuite que les x_vars et y_vars choisis
            self.x_train = [train_client[self.xargs] for train_client in train_data]
            self.y_train = [train_client[self.yargs] for train_client in train_data]
            self.x_test = [test_client[self.xargs] for test_client in test_data]
            self.y_test = [test_client[self.yargs] for test_client in test_data]

    def train_model(self):
        if not self.group:
            self.model.fit(self.x_train, np.array(self.y_train).ravel())
        else:
            for i, model in enumerate(self.model):
                model.fit(self.x_train[i], np.array(self.y_train[i]).ravel())

    def test_model(self):
        if not self.group:
            self.y_pred = self.model.predict(self.x_test)
        else:
            self.y_pred = []
            for i, model in enumerate(self.model):
                self.y_pred.append(model.predict(self.x_test[i]).ravel())

    def performance_indicator(self):
        self.evaluation_model = []
        if not self.group:
            perf = pd.DataFrame(self.y_test.copy())
            perf["prediction"] = self.y_pred
            perf["id_client"] = self.df["id_client"]

            for i in self.df["id_client"].unique():
                y = perf.groupby("id_client").get_group(i)["prediction"]
                y2 = np.array(
                    perf.groupby("id_client").get_group(i)[self.yargs]
                ).ravel()
                self.evaluation_model.append(metrics(y2, y))
        else:
            for i in range(len(self.clients)):
                self.evaluation_model.append(
                    metrics(
                        np.array(self.y_test[i]).ravel(),
                        np.array(self.y_pred[i]).ravel(),
                    )
                )

    def complet_process(self):
        x1, x2, x3 = self.best_lim_date()
        self.lim_date = x3
        self.generate_model()
        self.generate_train_set()
        self.train_model()
        self.test_model()
        self.performance_indicator()
