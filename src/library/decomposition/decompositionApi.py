import pandas as pd

from src.library.decomposition._decompositionBusinessLogic import _decompose_image_wrapper, \
    _print_explained_variance_ratio
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum


class DecompositionApi:
    @staticmethod
    def decompose_image_wrapper(df: pd.DataFrame, decomposition_type: DecompositionEnum,
                                fast_ica_n_components=None) -> pd.DataFrame:
        return _decompose_image_wrapper(df, decomposition_type, fast_ica_n_components)

    @staticmethod
    def print_explained_variance_ratio(df: pd.DataFrame):
        _print_explained_variance_ratio(df)
