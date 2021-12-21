import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA, FastICA, NMF

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelData import ChannelData
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.properties.properties import PCA_VARIATION_MIN_VALUE, DECOMPOSED_CHANNEL_NAME_TEMPLATE, \
    STANDARIZED_CHANNEL_NAME_TEMPLATE
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData
from src.library.standarization.standarizationApi import StandarizationApi


def _decompose_channel_wrapper(df: pd.DataFrame, channels_data_map: [ChannelData],
                               decomposed_channels_data_map: [DecomposedChannelData],
                               standarized_channels_data_map: [StandarizedChannelData],
                               channel_name: str, decomposition_type: DecompositionEnum,
                               take_standarized_channel: bool,
                               fast_ica_n_components=None) -> (pd.DataFrame, [DecomposedChannelData]):
    # PCA has good mechanism to calculate n_components automatically

    channel_data = ChannelApi.find_channel_by_name(channels_data_map, channel_name)

    if take_standarized_channel:
        if StandarizationApi.is_channel_standarized(channel_name, standarized_channels_data_map):
            actual_channel_name_for_decomposition = STANDARIZED_CHANNEL_NAME_TEMPLATE + channel_name
        else:
            print("Channel ", channel_name, " was not standarized - taking not standarized values")
            actual_channel_name_for_decomposition = channel_name
    else:
        actual_channel_name_for_decomposition = channel_name

    channel_to_decompose_df = pd.DataFrame(data=df[actual_channel_name_for_decomposition].to_numpy()
                                           .reshape(channel_data.width, channel_data.height))
    channel_to_decompose_df.attrs['channel_name'] = channel_name
    if decomposition_type == DecompositionEnum.PCA:
        transformed_channel_df, decomposed_channel_data = _transform_pca(
            channel_to_decompose_df, take_standarized_channel)
    elif decomposition_type == DecompositionEnum.NMF:
        n_components = _calculate_no_components_using_pca(df)
        transformed_channel_df, decomposed_channel_data = _transform_nmf(
            channel_to_decompose_df, n_components, take_standarized_channel)
    elif decomposition_type == DecompositionEnum.FAST_ICA:
        if not fast_ica_n_components:
            raise Exception("ERROR: Fast Ica requires n_components input from the user!")
        transformed_channel_df, decomposed_channel_data = _transform_ica(
            channel_to_decompose_df, fast_ica_n_components, take_standarized_channel)
    else:
        raise Exception("Chosen Decomposition type is not allowed")

    transformed_channel_df.columns = [DECOMPOSED_CHANNEL_NAME_TEMPLATE + channel_name]
    decomposed_channels_data_map.append(decomposed_channel_data)
    return pd.concat([df, transformed_channel_df], axis=1), decomposed_channels_data_map


# TODO: transformation type in name to make multiple transformations possible for a channel
def _transform_pca(df: pd.DataFrame, from_standarized_channel: bool) -> (pd.DataFrame, DecomposedChannelData):
    pca = PCA(svd_solver='full', n_components=PCA_VARIATION_MIN_VALUE)
    principal_components = pca.fit_transform(df)
    principal_df = pd.DataFrame(data=principal_components.flatten())
    return principal_df, DecomposedChannelData(df.attrs['channel_name'], pca,
                                               DECOMPOSED_CHANNEL_NAME_TEMPLATE + df.attrs['channel_name'],
                                               from_standarized_channel)


def _transform_ica(df: pd.DataFrame, n_components: int, from_standarized_channel: bool
                   ) -> (pd.DataFrame, DecomposedChannelData):
    ica = FastICA(n_components=n_components)
    independent_components = ica.fit_transform(df)
    independent_df = pd.DataFrame(data=independent_components.flatten())
    return independent_df, DecomposedChannelData(df.attrs['channel_name'], ica,
                                                 DECOMPOSED_CHANNEL_NAME_TEMPLATE + df.attrs['channel_name'],
                                                 from_standarized_channel)


def _transform_nmf(df: pd.DataFrame, n_components: int, from_standarized_channel: bool
                   ) -> (pd.DataFrame, DecomposedChannelData):
    nmf = NMF(n_components=n_components)
    nmf_components = nmf.fit_transform(df)
    nmf_df = pd.DataFrame(data=nmf_components.flatten())
    return nmf_df, DecomposedChannelData(df.attrs['channel_name'], nmf,
                                         DECOMPOSED_CHANNEL_NAME_TEMPLATE + df.attrs['channel_name'],
                                         from_standarized_channel)


# returns different result than automatic mode
def _calculate_no_components_using_pca(df: pd.DataFrame):
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


def _print_explained_variance_ratio(df: pd.DataFrame):
    pca = PCA().fit(df)
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.xlim([0, 5])
    plt.ylabel('cumulative explained variance')
    plt.gcf().set_size_inches(7, 5)
    plt.axhline(y=PCA_VARIATION_MIN_VALUE, color='r', linestyle='-')

    plt.show()
