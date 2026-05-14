from app.config.training_config import TRAINING_CONFIG
from copy import deepcopy


# Copia editable en memoria
RUNTIME_CONFIG = deepcopy(TRAINING_CONFIG)


def get_config():
    return RUNTIME_CONFIG


def update_config(updates: dict):
    """
    Mezcla recursivamente los cambios del admin con la config actual.
    """
    def merge(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and k in d:
                merge(d[k], v)
            else:
                d[k] = v
        return d

    merge(RUNTIME_CONFIG, updates)
    return RUNTIME_CONFIG
