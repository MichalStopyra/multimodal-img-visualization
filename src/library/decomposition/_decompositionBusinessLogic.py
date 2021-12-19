import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA, FastICA, NMF

from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.properties.properties import PCA_VARIATION_MIN_VALUE, DECOMPOSED_CHANNEL_NAME_TEMPLATE


def _decompose_image_wrapper(df: pd.DataFrame, decomposition_type: DecompositionEnum,
                             fast_ica_n_components=None) -> pd.DataFrame:
    # PCA has good mechanism to calculate n_components automatically
    if decomposition_type == DecompositionEnum.PCA:
        return _transform_pca(df)
    elif decomposition_type == DecompositionEnum.NMF:
        n_components = _calculate_no_components_using_pca(df)
        return _transform_nmf(df, n_components)
    elif decomposition_type == DecompositionEnum.FAST_ICA:
        if not fast_ica_n_components:
            raise Exception("ERROR: Fast Ica requires n_components input from the user!")
        return _transform_ica(df, fast_ica_n_components)

    raise Exception("Chosen Decomposition type is not allowed")


def _transform_pca(df: pd.DataFrame) -> pd.DataFrame:
    pca = PCA(svd_solver='full', n_components=PCA_VARIATION_MIN_VALUE)
    principal_components = pca.fit_transform(df)
    principal_df = pd.DataFrame(data=principal_components)
    principal_df.columns = [DECOMPOSED_CHANNEL_NAME_TEMPLATE + f'{i}' for i in range(1, 1 + principal_df.shape[1])]
    return principal_df


def _transform_ica(df: pd.DataFrame, n_components: int) -> pd.DataFrame:
    ica = FastICA(n_components=n_components)
    independent_components = ica.fit_transform(df)
    independent_df = pd.DataFrame(data=independent_components)
    independent_df.columns = [DECOMPOSED_CHANNEL_NAME_TEMPLATE + f'{i}' for i in range(1, 1 + independent_df.shape[1])]
    return independent_df


def _transform_nmf(df: pd.DataFrame, n_components: int) -> pd.DataFrame:
    nmf = NMF(n_components=n_components)
    nmf_components = nmf.fit_transform(df)
    nmf_df = pd.DataFrame(data=nmf_components)
    nmf_df.columns = [DECOMPOSED_CHANNEL_NAME_TEMPLATE + f'{i}' for i in range(1, 1 + nmf_df.shape[1])]
    return nmf_df


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
