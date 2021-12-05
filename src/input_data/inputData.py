import numpy as np
import pandas as pd

from src.input_data.fileReader import FileReader
from sklearn.decomposition import PCA, FastICA, NMF

from src.utils.DecompositionEnum import Decomposition
from src.utils.constants import *

import matplotlib.pyplot as plt



def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        df[column] = df[column].astype(float)

    # normalized_df = (df - df.mean()) / df.std()
    normalized_df = (df - df.min()) / (df.max() - df.min())
    return normalized_df


def transform_pca(df: pd.DataFrame) -> pd.DataFrame:
    pca = PCA(svd_solver='full', n_components=PCA_VARIATION_MIN_VALUE)
    principal_components = pca.fit_transform(df)
    principal_df = pd.DataFrame(data=principal_components)
    principal_df.columns = [f'principal component{i}' for i in range(1, 1 + principal_df.shape[1])]
    return principal_df


def transform_ica(df: pd.DataFrame) -> pd.DataFrame:
    ica = FastICA(n_components=3)
    independent_components = ica.fit_transform(df)
    independent_df = pd.DataFrame(data=independent_components)
    independent_df.columns = [f'independent component{i}' for i in range(1, 1 + independent_df.shape[1])]
    return independent_df


def transform_nmf(df: pd.DataFrame) -> pd.DataFrame:
    nmf = NMF(n_components=3)
    nmf_components = nmf.fit_transform(df)
    nmf_df = pd.DataFrame(data=nmf_components)
    nmf_df.columns = [f'nmf component{i}' for i in range(1, 1 + nmf_df.shape[1])]
    return nmf_df


# Works only for PCA
def print_explained_variance_ratio(df: pd.DataFrame):
    pca = PCA().fit(df)
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.xlim([0,5])
    plt.ylabel('cumulative explained variance')
    plt.gcf().set_size_inches(7, 5)
    plt.show()

def transform_image_wrapper(df: pd.DataFrame, decomposition_type: Decomposition) -> pd.DataFrame:
    if decomposition_type == Decomposition.PCA:
        return transform_pca(df)
    elif decomposition_type == Decomposition.ICA:
        return transform_ica(df)
    elif decomposition_type == Decomposition.NMF:
        return transform_nmf(df)

    raise Exception("Chosen transformation type is not allowed")


class InputData:

    # class used for normalizing data
    # sci-kit learn functions do not handle empty attributes values - they need to be handled here
    def __init__(self, file_path):
        self.file_reader = FileReader(file_path)

        # TODO: add standarising functions to test and validation sets
        self.image_df = normalize_data(self.file_reader.input_df)
        print(self.image_df.describe())

        self.image_df_pca = transform_image_wrapper(self.image_df, Decomposition.PCA)
        # self.image_df_ica = transform_image_wrapper(self.image_df, Transformation.ICA)
        # self.image_df_nmf = transform_image_wrapper(self.image_df, Transformation.NMF)
        print(self.image_df_pca.head())
        print_explained_variance_ratio(self.image_df)
        # print(self.image_df_ica)
        # print(self.image_df_nmf)
