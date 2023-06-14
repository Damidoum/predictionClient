import matplotlib.pyplot as plt
from metrics import export_mesure
from model_objet import Model


def display_mesure(data, eval_model_list, titles):
    """
    description : permet de faire l'affichage de la moyenne des R2, MSE, MAE pour chaque client.
    paramètres :
    - data : DataFrame des données
    - eval_model_list
    """

    X = data["id_client"].unique()

    fig, ax = plt.subplots(3, figsize=(10, 10))
    ax[0].set_title("R2")
    ax[1].set_title("MSE")
    ax[2].set_title("MAE")
    for eval_model, title in zip(eval_model_list, titles):
        r2, mse, mae = export_mesure(eval_model)
        ax[0].plot(X, r2, label=title)
        ax[0].legend()
        ax[1].plot(X, mse, label=title)
        ax[1].legend()
        ax[2].plot(X, mae, label=title)
        ax[2].legend()
    return fig, ax


def display_prediction(Model, i):
    id_client = Model.df["id_client"].unique()[i]
    df_display = Model.df[Model.df["horodate"] > Model.date_lim][
        [
            "id_client",
            "real_consumption",
            "prediction",
            "horodate",
            "forecasted_consumption",
        ]
    ].copy()
    df_display.rename({"prediction": "prediction_airliquide"}, axis=1, inplace=True)

    # récupération de la prédiction du client
    if not Model.group:
        df_display["prediction"] = Model.y_pred.copy()
        df_display.groupby("id_client").get_group(id_client).plot(
            x="horodate", y=["prediction", "real_consumption", "forecasted_consumption"]
        )
    else:
        df_display = df_display.groupby("id_client").get_group(id_client)
        df_display["prediction"] = Model.y_pred[i].copy()
        df_display.plot(
            x="horodate", y=["prediction", "real_consumption", "forecasted_consumption"]
        )
