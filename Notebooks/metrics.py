from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pandas as pd


def metrics(y_true, y_pred):
    # Calculer le coefficient de détermination (R²)
    r2 = r2_score(y_true, y_pred)

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
