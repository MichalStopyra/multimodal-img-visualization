import decimal
from typing import Dict

import numpy as np
import pandas as pd

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelData import ChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.properties.properties import STANDARIZED_CHANNEL_NAME_TEMPLATE, DESTANDARIZED_CHANNEL_NAME_TEMPLATE, \
    REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE, DESTANDARIZED_AFTER_DECOMPOSITION_CHANNEL_NAME_TEMPLATE
from src.library.standarization.dto.destandarizedChannelData import DestandarizedChannelData
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData
from src.library.standarization.enum.standarizationModeEnum import StandarizationModeEnum


def _standarize_image_channels(df: pd.DataFrame, channels_to_exclude: [str],
                               channels_data_map: [ChannelData],
                               standarized_channels_data_map: [StandarizedChannelData],
                               standarization_modes: Dict[str, StandarizationModeEnum] = None
                               ) -> (pd.DataFrame, [StandarizedChannelData]):
    if standarization_modes is None:
        standarization_modes = {}

    for column in df.columns:

        if column in channels_to_exclude or _is_channel_standarized(column, standarized_channels_data_map):
            continue

        channel_data = ChannelApi.find_channel_by_name(channels_data_map, column)

        # if standarization_modes doesn't contain specified channel - channel min max mode by default
        # else according to the chosen mode
        if column in standarization_modes and \
                standarization_modes[column] == StandarizationModeEnum.BIT_SIZE_MIN_MAX:
            max_value = std_channel_multiplier = np.power(2, channel_data.bit_size) - 1
            min_value = 0
        else:
            max_value = std_channel_multiplier = df[column].max()
            min_value = df[column].min()

        standarized_column_df = pd.DataFrame(data=((df[column] - min_value) / (max_value - min_value)))
        standarized_column_df.columns = [STANDARIZED_CHANNEL_NAME_TEMPLATE + column]
        standarized_channels_data_map.append(
            StandarizedChannelData(column, STANDARIZED_CHANNEL_NAME_TEMPLATE + column, std_channel_multiplier))

        df = pd.concat([df, standarized_column_df], axis=1)

    return df, standarized_channels_data_map


def _destandarize_channel(df: pd.DataFrame, initial_channel_name: str, after_reverse_decomposition: bool,
                          standarized_channels_data_map: [StandarizedChannelData],
                          destandarized_channels_data_map: [DestandarizedChannelData],
                          rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData],
                          ) -> (pd.DataFrame, [DestandarizedChannelData]):
    # Needs to be standarized to be destandarized
    std_channel_data = _find_channel_data_in_map_by_initial_name(initial_channel_name, standarized_channels_data_map)
    if not std_channel_data:
        print("Channel was not standarized! returning with no changes applied")
        return df, destandarized_channels_data_map

    # If destandarizing after rvrs decomposition - check if rvrs decomposition was actually performed
    if after_reverse_decomposition:
        rvrs_decomposed_channel_data = _find_channel_data_in_map_by_initial_name(
            initial_channel_name, rvrs_decomposed_channels_data_map)
        if not rvrs_decomposed_channel_data:
            print("Channel was not reversly decomposed! returning with no changes applied")
            return df, destandarized_channels_data_map

        channel_to_destandarize_name = REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE + initial_channel_name
    else:
        channel_to_destandarize_name = STANDARIZED_CHANNEL_NAME_TEMPLATE + initial_channel_name

    std_channel_array = df[channel_to_destandarize_name].to_numpy().astype(float)

    multiplier_float = float(std_channel_data.standarization_multiplier)

    std_channel_array = (np.round(std_channel_array * multiplier_float, 0) % multiplier_float) \
        .astype("str").astype(decimal.Decimal)

    destandarized_channel_df = pd.DataFrame(data=std_channel_array)
    column_final_name = DESTANDARIZED_AFTER_DECOMPOSITION_CHANNEL_NAME_TEMPLATE + initial_channel_name \
        if after_reverse_decomposition \
        else DESTANDARIZED_CHANNEL_NAME_TEMPLATE + initial_channel_name
    destandarized_channel_df.columns = [column_final_name]

    destandarized_channels_data_map.append(
        DestandarizedChannelData(initial_channel_name, column_final_name, after_reverse_decomposition))
    return pd.concat([df, destandarized_channel_df], axis=1), destandarized_channels_data_map


def _is_channel_standarized(initial_channel_name: str, std_channels_data_map: [StandarizedChannelData]
                            ) -> bool:
    map_element_list = list(filter(
        lambda channel: channel.initial_channel_name == initial_channel_name, std_channels_data_map))

    return map_element_list is not None and len(map_element_list) != 0


def _find_channel_data_in_map_by_initial_name(initial_channel_name: str,
                                              std_channels_data_map: [any]
                                              ) -> any:
    map_element_list = list(filter(
        lambda channel: channel.initial_channel_name == initial_channel_name, std_channels_data_map))

    return map_element_list[0] if map_element_list is not None and len(map_element_list) == 1 else None
