from typing import Dict

import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.library.standarization._standarizationBusinessLogic import _standarize_image_channels, \
    _destandarize_channel, _is_channel_standarized, _find_std_channel_data_by_name
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
    def destandarize_channel(df: pd.DataFrame, original_channel_name: str,
                             standarized_channels_data_map: [StandarizedChannelData],
                             destandarized_channels_data_map: [DestandarizedChannelData]
                             ) -> (pd.DataFrame, [DestandarizedChannelData]):
        return _destandarize_channel(df, original_channel_name,
                                     standarized_channels_data_map, destandarized_channels_data_map)

    @staticmethod
    def is_channel_standarized(original_channel_name: str, std_channels_data_map: [StandarizedChannelData]
                               ) -> bool:
        return _is_channel_standarized(original_channel_name, std_channels_data_map)

    @staticmethod
    def find_std_channel_data_by_name(original_channel_name: str, std_channels_data_map: [StandarizedChannelData]
                                      ) -> StandarizedChannelData:
        return _find_std_channel_data_by_name(original_channel_name, std_channels_data_map)
