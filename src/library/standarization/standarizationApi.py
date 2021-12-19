from typing import Dict

import numpy as np
import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.library.standarization._standarizationBusinessLogic import _standarize_image_channels, _destandarize_channel
from src.library.standarization.enum.standarizationModeEnum import StandarizationModeEnum


class StandarizationApi:

    @staticmethod
    def standarize_image_channels(df: pd.DataFrame, channels_to_exclude: [str],
                                  channels_data_map: [ChannelData],
                                  standarization_modes: Dict[str, StandarizationModeEnum] = None
                                  ) -> (pd.DataFrame, [ChannelData]):
        return _standarize_image_channels(df, channels_to_exclude, channels_data_map, standarization_modes)

    @staticmethod
    def destandarize_channel(channel_array: np.ndarray, channel_data: ChannelData) -> np.ndarray:
        return _destandarize_channel(channel_array, channel_data)
