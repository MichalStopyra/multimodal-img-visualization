import numpy as np
import pandas as pd
from typing import Dict

from src.input_data.channel.channelInput import ChannelInputInterface
from src.input_data.channel.channelNameAndBitSize import ChannelNameAndBitSize
from src.input_data.multimodalImage import MultimodalImage
from sklearn.decomposition import PCA, FastICA, NMF

from src.input_data.standarization.standarizationModeEnum import StandarizationModeEnum
from src.utils.decompositionEnum import Decomposition
from src.utils.constants import *

import matplotlib.pyplot as plt


def normalize_data(df: pd.DataFrame, channels_to_exclude: [str],
                   standarization_modes: Dict[str, StandarizationModeEnum],
                   channels_name_bit_size_map: [ChannelNameAndBitSize]) -> pd.DataFrame:
    result = df.copy()
    for column in df.columns:
        if column in channels_to_exclude:
            continue

        df[column] = df[column].astype(float)

        # if standarization_modes doesn't contain specified channel - channel min max mode by default
        # else according to the chosen mode
        if column in standarization_modes and \
                standarization_modes[column] == StandarizationModeEnum.BIT_SIZE_MIN_MAX:
            map_element = list(filter(lambda cnbz: cnbz.name == column, channels_name_bit_size_map))
            if not map_element or len(map_element) != 1:
                raise Exception("Channel: {}'s bit size not specified", column)

            max_value = np.power(2, map_element[0].bit_size) - 1
            min_value = 0
        else:
            max_value = df[column].max()
            min_value = df[column].min()

        result[column] = (df[column] - min_value) / (max_value - min_value)

    return result


def transform_pca(df: pd.DataFrame) -> pd.DataFrame:
    pca = PCA(svd_solver='full', n_components=PCA_VARIATION_MIN_VALUE)
    principal_components = pca.fit_transform(df)
    principal_df = pd.DataFrame(data=principal_components)
    principal_df.columns = [f'principal component{i}' for i in range(1, 1 + principal_df.shape[1])]
    return principal_df


def transform_ica(df: pd.DataFrame, n_components: int) -> pd.DataFrame:
    ica = FastICA(n_components=n_components)
    independent_components = ica.fit_transform(df)
    independent_df = pd.DataFrame(data=independent_components)
    independent_df.columns = [f'independent component{i}' for i in range(1, 1 + independent_df.shape[1])]
    return independent_df


def transform_nmf(df: pd.DataFrame, n_components: int) -> pd.DataFrame:
    nmf = NMF(n_components=n_components)
    nmf_components = nmf.fit_transform(df)
    nmf_df = pd.DataFrame(data=nmf_components)
    nmf_df.columns = [f'nmf component{i}' for i in range(1, 1 + nmf_df.shape[1])]
    return nmf_df


def print_explained_variance_ratio(df: pd.DataFrame):
    pca = PCA().fit(df)
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.xlim([0, 5])
    plt.ylabel('cumulative explained variance')
    plt.gcf().set_size_inches(7, 5)
    plt.axhline(y=PCA_VARIATION_MIN_VALUE, color='r', linestyle='-')

    plt.show()


# returns different result than automatic mode
def calculate_no_components_using_pca(df: pd.DataFrame):
    pca = PCA().fit(df)

    xi = np.arange(0, df.shape[1], step=1)
    y = np.cumsum(pca.explained_variance_ratio_)

    xa = plt.plot(xi, y)
    y_values = xa[0].get_ydata()

    n_components = 1
    for x, y in enumerate(y_values):
        n_components = x
        if y >= PCA_VARIATION_MIN_VALUE:
            break
    return n_components


def transform_image_wrapper(df: pd.DataFrame, decomposition_type: Decomposition,
                            fast_ica_n_components=None) -> pd.DataFrame:
    # PCA has good mechanism to calculate n_components automatically
    if decomposition_type == Decomposition.PCA:
        return transform_pca(df)
    elif decomposition_type == Decomposition.NMF:
        n_components = calculate_no_components_using_pca(df)
        return transform_nmf(df, n_components)
    elif decomposition_type == Decomposition.FAST_ICA:
        if not fast_ica_n_components:
            raise Exception("ERROR: Fast Ica requires n_components input from the user!")
        return transform_ica(df, fast_ica_n_components)

    raise Exception("Chosen Decomposition type is not allowed")


class InputData:

    # class used for normalizing data
    # sci-kit learn functions do not handle empty attributes values - they need to be handled here
    def __init__(self, channels_inputs: [ChannelInputInterface]):
        self.file_reader = MultimodalImage(channels_inputs)
        self.image_df = self.file_reader.input_df
        self.channels_name_bit_size_map = self.file_reader.channels_name_bit_size_map

        self.normalize_data(['r'], {'r1': StandarizationModeEnum.BIT_SIZE_MIN_MAX})
        # print(self.image_df.describe())

        # self.image_df_pca = transform_image_wrapper(self.image_df, Decomposition.PCA)
        # self.image_df_ica = transform_image_wrapper(self.image_df, Decomposition.FAST_ICA, 3)
        # self.image_df_nmf = transform_image_wrapper(self.image_df, Decomposition.NMF)
        # print(self.image_df_pca.head())
        # print_explained_variance_ratio(self.image_df)
        # print(self.image_df_ica)
        # print(self.image_df_nmf)

    def normalize_data(self, channels_to_exclude: [str],
                       standarization_modes: Dict[str, StandarizationModeEnum] = None):
        if standarization_modes is None:
            standarization_modes = {}

        self.image_df = normalize_data(self.file_reader.input_df, channels_to_exclude,
                                       standarization_modes, self.channels_name_bit_size_map)
