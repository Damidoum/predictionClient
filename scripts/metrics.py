from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.inspection import permutation_importance
import pandas as pd
from typing import List, Tuple
import numpy as np


def metrics(y_true, y_pred):
    # Calculer le coefficient de détermination (R²)
    # r2 = r2_score(y_true, y_pred)

    correlation_matrix = np.corrcoef(y_true, y_pred)
    correlation = correlation_matrix[0, 1]
    r2 = correlation**2

    # Calculer l'erreur quadratique moyenne (EQM)
    mse = mean_squared_error(y_true, y_pred)

    # Calculer l'erreur absolue moyenne (EAM)
    mae = mean_absolute_error(y_true, y_pred)

    return (r2, mse, mae)


def export_mesure(eval_model):
    r2 = [x[0] for x in eval_model]
    mse = [x[1] for x in eval_model]
    mae = [x[2] for x in eval_model]
    return r2, mse, mae


def tab_mesure(eval_model):
    r2, mse, mae = export_mesure(eval_model)
    df = pd.DataFrame({"R2": r2, "MSE": mse, "MAE": mae})
    return df


from creation_model import complet_process


def permutation_feature_importance(
    df: pd.DataFrame,
    xargs: List[str],
    yargs: List[str],
    lim_date: float,
    random_forest=False,
    n_estimators=150,
):
    """description : calcul des features importances"""
    model, eval_model = complet_process(
        df, xargs, yargs, lim_date, False, random_forest, n_estimators
    )

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
    X_test = test.copy()[xargs]
    Y_test = test.copy()[yargs]

    result = permutation_importance(
        model, X_test, Y_test, n_repeats=100, random_state=42
    )

    # Récupération des scores d'importance
    importance_scores = result.importances_mean

    return importance_scores
