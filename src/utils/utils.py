import numpy as np


def pixel_values_array_from_csv(csv_path: str) -> np.ndarray:
    return np.genfromtxt(csv_path, dtype=np.uint8, delimiter=",")
