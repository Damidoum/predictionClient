import nbformat as nbf
import re
from import_data import import_data_complete
from nbconvert.preprocessors import ExecutePreprocessor
import os 

os.chdir("../notebooks/clients/")

data = import_data_complete(path = "../../")
clients = data["id_client"].unique()

# Nom du notebook d'origine
original_notebook_path = "client1.ipynb"

# Pattern à rechercher et remplacer dans le notebook
pattern1 = r"# Étude du client (\d+)"
pattern2 = r"client = (\d+)"


# Charger le notebook d'origine
with open(original_notebook_path, "r", encoding="utf-8") as f:
    notebook = nbf.read(f, as_version=nbf.NO_CONVERT)

# Pour chaque nouveau dataframe
for i in clients[1:] :
    # Copier le notebook d'origine
    new_notebook = notebook.copy()
    cells = new_notebook.cells 
    cell = cells[0]
    cell.source = re.sub(pattern1, f"# Étude du client {i}", cell.source)
    cell = cells[4]
    cell.source = re.sub(pattern2, f"client = {i}", cell.source)


    # Enregistrer le nouveau notebook
    new_notebook_path = f"client_{i}.ipynb"

    # Créer un exécuteur pour exécuter le notebook
    executeur = ExecutePreprocessor(timeout=None)

    # Exécuter le notebook
    executeur.preprocess(new_notebook)

    # Enregistrer les modifications dans le notebook
    with open(new_notebook_path, "w", encoding="utf-8") as f:
        nbf.write(new_notebook, f)
    print(f"Notebook {i} créé avec succès.")






