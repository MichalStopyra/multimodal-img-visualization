import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA, FastICA, NMF

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelData import ChannelData
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.properties.properties import PCA_VARIATION_MIN_VALUE, DECOMPOSED_CHANNEL_NAME_TEMPLATE


def _decompose_channel_wrapper(df: pd.DataFrame, channels_data_map: [ChannelData],
                               decomposed_channels_data_map: [DecomposedChannelData],
                               channel_name: str, decomposition_type: DecompositionEnum,
                               fast_ica_n_components=None) -> (pd.DataFrame, DecomposedChannelData):
    # PCA has good mechanism to calculate n_components automatically

    # TODO: add resolution param
    channel_data = ChannelApi.find_channel_by_name(channels_data_map, channel_name)
    channel_to_decompose_df = pd.DataFrame(data=df[channel_name].to_numpy()
                                           .reshape(channel_data.width, channel_data.height))
    channel_to_decompose_df.attrs['channel_name'] = channel_name
    if decomposition_type == DecompositionEnum.PCA:
        transformed_channel_df, decomposed_channel_data = _transform_pca(channel_to_decompose_df)
    elif decomposition_type == DecompositionEnum.NMF:
        n_components = _calculate_no_components_using_pca(df)
        transformed_channel_df, decomposed_channel_data = _transform_nmf(channel_to_decompose_df, n_components)
    elif decomposition_type == DecompositionEnum.FAST_ICA:
        if not fast_ica_n_components:
            raise Exception("ERROR: Fast Ica requires n_components input from the user!")
        transformed_channel_df, decomposed_channel_data = _transform_ica(channel_to_decompose_df, fast_ica_n_components)
    else:
        raise Exception("Chosen Decomposition type is not allowed")

    transformed_channel_df.columns = [DECOMPOSED_CHANNEL_NAME_TEMPLATE + channel_name]
    decomposed_channels_data_map.append(decomposed_channel_data)
    return pd.concat([df, transformed_channel_df], axis=1), decomposed_channels_data_map


def _transform_pca(df: pd.DataFrame) -> (pd.DataFrame, DecomposedChannelData):
    pca = PCA(svd_solver='full', n_components=PCA_VARIATION_MIN_VALUE)
    principal_components = pca.fit_transform(df)
    principal_df = pd.DataFrame(data=principal_components.flatten())
    return principal_df, DecomposedChannelData(df.attrs['channel_name'], pca)


def _transform_ica(df: pd.DataFrame, n_components: int) -> (pd.DataFrame, DecomposedChannelData):
    ica = FastICA(n_components=n_components)
    independent_components = ica.fit_transform(df)
    independent_df = pd.DataFrame(data=independent_components.flatten())
    return independent_df, DecomposedChannelData(df.attrs['channel_name'], ica)


def _transform_nmf(df: pd.DataFrame, n_components: int) -> (pd.DataFrame, DecomposedChannelData):
    nmf = NMF(n_components=n_components)
    nmf_components = nmf.fit_transform(df)
    nmf_df = pd.DataFrame(data=nmf_components.flatten())
    return nmf_df, DecomposedChannelData(df.attrs['channel_name'], nmf)


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

#
# def __add_decomposed_channels_data_to_channels_map(channels_data_map: [ChannelData], columns: [str]):
#     for column in columns:
#         channels_data_map.append(ChannelData(column, ))
