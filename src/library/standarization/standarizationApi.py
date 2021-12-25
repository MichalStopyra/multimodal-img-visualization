from typing import Dict

import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.standarization._standarizationBusinessLogic import _standarize_image_channels, \
    _destandarize_channel, _is_channel_standarized, _find_channel_data_in_map_by_initial_name
from src.library.standarization.dto.destandarizedChannelData import DestandarizedChannelData
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData
from src.library.standarization.enum.standarizationModeEnum import StandarizationModeEnum


class StandarizationApi:

    @staticmethod
    def standarize_image_channels(df: pd.DataFrame, channels_to_exclude: [str],
                                  channels_data_map: [ChannelData],
                                  standarized_channels_data_map: [StandarizedChannelData],
                                  standarization_modes: Dict[str, StandarizationModeEnum] = None
                                  ) -> (pd.DataFrame, [StandarizedChannelData]):
        return _standarize_image_channels(df, channels_to_exclude, channels_data_map,
                                          standarized_channels_data_map, standarization_modes)

    @staticmethod
    def destandarize_channel(df: pd.DataFrame, initial_channel_name: str, after_reverse_decomposition: bool,
                             standarized_channels_data_map: [StandarizedChannelData],
                             destandarized_channels_data_map: [DestandarizedChannelData],
                             rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData],
                             ) -> (pd.DataFrame, [DestandarizedChannelData]):
        return _destandarize_channel(df, initial_channel_name, after_reverse_decomposition,
                                     standarized_channels_data_map, destandarized_channels_data_map,
                                     rvrs_decomposed_channels_data_map)

    @staticmethod
    def is_channel_standarized(initial_channel_name: str, std_channels_data_map: [StandarizedChannelData]
                               ) -> bool:
        return _is_channel_standarized(initial_channel_name, std_channels_data_map)

    @staticmethod
    def find_std_channel_data_by_name(initial_channel_name: str, std_channels_data_map: [StandarizedChannelData]
                                      ) -> StandarizedChannelData:
        return _find_channel_data_in_map_by_initial_name(initial_channel_name, std_channels_data_map)
