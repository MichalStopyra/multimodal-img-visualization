import pandas as pd

from src.data_container.decomposed_image.decomposedImage import DecomposedImage
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.properties.properties import REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE, DECOMPOSED_CHANNEL_NAME_TEMPLATE


def _reverse_decompose_channel(df: pd.DataFrame, channel_name: str, decomposed_channels_data: [DecomposedChannelData],
                               rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData]
                               ) -> (pd.DataFrame, [ReverseDecomposedChannelData]):
    decomposed_channel_data = __get_decomposed_channel_data(decomposed_channels_data, channel_name)

    channel_to_reverse_decompose_df = __prepare_channel_to_reverse_decompose_df(channel_name, decomposed_channel_data,
                                                                                df)

    reverse_decomposed_channel_array = decomposed_channel_data.decomposition_object.inverse_transform(
        channel_to_reverse_decompose_df).flatten()

    reverse_decomposed_channel_df = pd.DataFrame(data=reverse_decomposed_channel_array)

    reverse_decomposed_channel_df.columns = [REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE + channel_name]
    rvrs_decomposed_channels_data_map.append(ReverseDecomposedChannelData(
        channel_name, REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE + channel_name,
        decomposed_channel_data.from_standarized_channel))

    return pd.concat([df, reverse_decomposed_channel_df], axis=1), rvrs_decomposed_channels_data_map


def _rvrs_decompose_image_channels(decomposed_image_data: DecomposedImage) -> pd.DataFrame:
    return decomposed_image_data.decomposition_object.inverse_transform(
        decomposed_image_data.decomposed_image_df)


def __get_decomposed_channel_data(decomposed_channels_data: [DecomposedChannelData], channel_name: str):
    data_list = list(filter(lambda dcd: dcd.initial_channel_name == channel_name, decomposed_channels_data))
    if not data_list or len(data_list) > 1:
        raise Exception("Not enough data to perform reverse decomposition")
    decomposed_channel_data = data_list[0]
    return decomposed_channel_data


def __prepare_channel_to_reverse_decompose_df(channel_name: str, decomposed_channel_data: DecomposedChannelData,
                                              df: pd.DataFrame) -> pd.DataFrame:
    shape = decomposed_channel_data.decomposition_object.components_.shape
    df_data_full = df[DECOMPOSED_CHANNEL_NAME_TEMPLATE + channel_name].to_numpy()
    df_data = df_data_full[0:(shape[0] * shape[1])].reshape(shape[1], shape[0])

    return pd.DataFrame(data=df_data)
