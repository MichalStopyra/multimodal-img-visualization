import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.decomposed_image.decomposedImage import DecomposedImage
from src.library.decomposition._decompositionBusinessLogic import _decompose_channel_resolution_wrapper, \
    _print_explained_variance_ratio, _decompose_image_channels_wrapper
from src.library.decomposition._reverseDecompositionBusinessLogic import _reverse_decompose_channel, \
    _rvrs_decompose_image_channels
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData


class DecompositionApi:
    @staticmethod
    def decompose_channel_resolution_wrapper(df: pd.DataFrame, channels_data_map: [ChannelData],
                                             decomposed_channels_data_map: [DecomposedChannelData],
                                             standarized_channels_data_map: [StandarizedChannelData],
                                             channel_name: str,
                                             decomposition_type: DecompositionEnum,
                                             take_standarized_channel: bool,
                                             fast_ica_n_components=None) -> (pd.DataFrame, [DecomposedChannelData]):
        return _decompose_channel_resolution_wrapper(df, channels_data_map, decomposed_channels_data_map,
                                                     standarized_channels_data_map,
                                                     channel_name, decomposition_type,
                                                     take_standarized_channel, fast_ica_n_components)

    @staticmethod
    def print_explained_variance_ratio(df: pd.DataFrame):
        _print_explained_variance_ratio(df)

    @staticmethod
    def reverse_decompose_channel(df: pd.DataFrame, channel_name: str,
                                  decomposed_channels_data: [DecomposedChannelData],
                                  rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData]
                                  ) -> (pd.DataFrame, [ReverseDecomposedChannelData]):
        return _reverse_decompose_channel(df, channel_name, decomposed_channels_data, rvrs_decomposed_channels_data_map)

    @staticmethod
    def decompose_image_channels_wrapper(df: pd.DataFrame,
                                         decomposition_type: DecompositionEnum,
                                         channel_names_and_take_std_tuple: [(str, bool)],
                                         standarized_channels_data_map: [StandarizedChannelData],
                                         fast_ica_n_components=None) -> DecomposedImage:
        return _decompose_image_channels_wrapper(df, decomposition_type, channel_names_and_take_std_tuple,
                                                 standarized_channels_data_map, fast_ica_n_components)

    @staticmethod
    def rvrs_decompose_image_channels(decomposed_image_data: DecomposedImage) -> pd.DataFrame:
        return _rvrs_decompose_image_channels(decomposed_image_data)
