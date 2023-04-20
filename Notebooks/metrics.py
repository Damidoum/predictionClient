from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np


def metrics(y_true, y_pred):
    # Calculer le coefficient de détermination (R²)
    r2 = r2_score(y_true, y_pred)

    # Calculer l'erreur quadratique moyenne (EQM)
    mse = mean_squared_error(y_true, y_pred)

    # Calculer l'erreur absolue moyenne (EAM)
    mae = mean_absolute_error(y_true, y_pred)

    return (r2, mse, mae)
