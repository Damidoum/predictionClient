from typing import List, Tuple


def make_train_test_set(
    clients: List, x_vars: List[str], y_vars: List[str]
) -> Tuple[List, List, List, List]:
    train_size = int(len(clients[0]) * 0.8)
    train_data = [client[:train_size] for client in clients]
    test_data = [client[train_size:] for client in clients]

    # on garde ensuite que les x_vars et y_vars choisis
    X_train = [train_client[x_vars] for train_client in train_data]
    y_train = [train_client[y_vars] for train_client in train_data]

    X_test = [test_client[x_vars] for test_client in test_data]
    y_test = [test_client[y_vars] for test_client in test_data]

    return X_train, X_test, y_train, y_test, test_data
