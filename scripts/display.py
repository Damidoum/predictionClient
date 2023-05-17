import matplotlib.pyplot as plt
from metrics import export_mesure


def display_mesure(data, eval_model_list, titles):
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
