import decimal
from typing import Dict

import numpy as np
import pandas as pd

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelData import ChannelData
from src.library.standarization.enum.standarizationModeEnum import StandarizationModeEnum


def _standarize_image_channels(df: pd.DataFrame, channels_to_exclude: [str],
                               channels_data_map: [ChannelData],
                               standarization_modes: Dict[str, StandarizationModeEnum] = None
                               ) -> (pd.DataFrame, [ChannelData]):
    if standarization_modes is None:
        standarization_modes = {}

    result = df.copy()
    for column in df.columns:
        df[column] = df[column].astype("string").apply(decimal.Decimal)

        if column in channels_to_exclude:
            continue

        channel_data = ChannelApi.find_channel_by_name(channels_data_map, column)

        # if standarization_modes doesn't contain specified channel - channel min max mode by default
        # else according to the chosen mode
        if column in standarization_modes and \
                standarization_modes[column] == StandarizationModeEnum.BIT_SIZE_MIN_MAX:
            max_value = np.power(2, channel_data.bit_size) - 1
            min_value = 0
        else:
            max_value = channel_data.max_value = df[column].max()
            min_value = df[column].min()

        result[column] = (df[column] - min_value) / (max_value - min_value)
        channel_data.standarized = True

    return result, channels_data_map


def _destandarize_channel(channel_array: np.ndarray, channel_data: ChannelData) -> np.ndarray:
    if not channel_data.standarized:
        return channel_array

    max_value_multiplier = float(channel_data.max_value if channel_data.max_value is not None \
                                     else np.power(2, channel_data.bit_size) - 1)
    return (np.round(channel_array * max_value_multiplier, 0) % max_value_multiplier).astype(np.uint8)
