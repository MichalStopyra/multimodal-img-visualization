import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.library.decomposition._decompositionBusinessLogic import _decompose_channel_wrapper, \
    _print_explained_variance_ratio
from src.library.decomposition._reverseDecompositionBusinessLogic import _reverse_decompose_channel
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData


class DecompositionApi:
    @staticmethod
    def decompose_channel_wrapper(df: pd.DataFrame, channels_data_map: [ChannelData],
                                  decomposed_channels_data_map: [DecomposedChannelData],
                                  standarized_channels_data_map: [StandarizedChannelData],
                                  channel_name: str,
                                  decomposition_type: DecompositionEnum,
                                  take_standarized_channel: bool,
                                  fast_ica_n_components=None) -> (pd.DataFrame, DecomposedChannelData):
        return _decompose_channel_wrapper(df, channels_data_map, decomposed_channels_data_map,
                                          standarized_channels_data_map,
                                          channel_name, decomposition_type,
                                          take_standarized_channel, fast_ica_n_components)

    @staticmethod
    def print_explained_variance_ratio(df: pd.DataFrame):
        _print_explained_variance_ratio(df)

    @staticmethod
    def reverse_decompose_channel(df: pd.DataFrame, channel_name: str, decomposed_channels_data: [DecomposedChannelData]
                                  ) -> pd.DataFrame:
        return _reverse_decompose_channel(df, channel_name, decomposed_channels_data)
