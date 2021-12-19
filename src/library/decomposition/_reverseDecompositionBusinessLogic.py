import pandas as pd
from sklearn.decomposition import PCA, NMF, FastICA

from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.properties.properties import REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE, DECOMPOSED_CHANNEL_NAME_TEMPLATE


def _reverse_decompose_channel(df: pd.DataFrame, channel_name: str, decomposed_channels_data: [DecomposedChannelData]) \
        -> pd.DataFrame:
    data_list = list(filter(lambda dcd: dcd.original_channel_name == channel_name, decomposed_channels_data))
    if not data_list or len(data_list) > 1:
        raise Exception("Not enough data to perform reverse decomposition")

    decomposed_channel_data = data_list[0]

    channel_to_reverse_decompose_df = __prepare_channel_to_reverse_decompose_df(channel_name, decomposed_channel_data,
                                                                                df)

    reverse_decomposed_channel_data = decomposed_channel_data.decomposition_object.inverse_transform(
        channel_to_reverse_decompose_df).flatten()

    reverse_decomposed_channel_df = pd.DataFrame(data=reverse_decomposed_channel_data)

    reverse_decomposed_channel_df.columns = [REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE + channel_name]
    return pd.concat([df, reverse_decomposed_channel_df], axis=1)


def __prepare_channel_to_reverse_decompose_df(channel_name: str, decomposed_channel_data: DecomposedChannelData,
                                              df: pd.DataFrame):
    shape = decomposed_channel_data.decomposition_object.components_.shape
    df_data_full = df[DECOMPOSED_CHANNEL_NAME_TEMPLATE + channel_name].to_numpy()
    df_data = df_data_full[0:(shape[0]*shape[1])] \
        .reshape(shape[1], shape[0])

    return pd.DataFrame(data=df_data)
