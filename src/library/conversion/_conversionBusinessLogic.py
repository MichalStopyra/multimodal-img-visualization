import decimal

import numpy as np
import pandas as pd
import polanalyser as pa

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelData import ChannelData
from src.library.constants.constants import CONVERTED_CHANNEL_INTENSITY_NAME_TEMPLATE, \
    CONVERTED_CHANNEL_DOLP_NAME_TEMPLATE, CONVERTED_CHANNEL_AOLP_H_NAME_TEMPLATE, \
    CONVERTED_CHANNEL_AOLP_S_NAME_TEMPLATE, CONVERTED_CHANNEL_AOLP_V_NAME_TEMPLATE, \
    CONVERTED_CHANNEL_AOLP_LIGHT_H_NAME_TEMPLATE, CONVERTED_CHANNEL_AOLP_LIGHT_S_NAME_TEMPLATE, \
    CONVERTED_CHANNEL_AOLP_LIGHT_V_NAME_TEMPLATE, CONVERTED_CHANNEL_AOLP_DARK_H_NAME_TEMPLATE, \
    CONVERTED_CHANNEL_AOLP_DARK_S_NAME_TEMPLATE, CONVERTED_CHANNEL_AOLP_DARK_V_NAME_TEMPLATE
from src.library.conversion.dto.ConvertedChannelData import ConvertedChannelData
from src.library.conversion.enum.conversionTypeEnum import ConversionTypeEnum


def _convert_channel(df: pd.DataFrame, channels_data_map: [ChannelData],
                     channel_name: str, conversion_type: ConversionTypeEnum,
                     converted_channels_data_map: [ConvertedChannelData]) -> (pd.DataFrame, [ConvertedChannelData]):
    channel_data = ChannelApi.find_channel_by_name_and_raise_exception(channels_data_map, channel_name)

    channel_to_polarize_array = df[channel_name].to_numpy().astype(np.uint8) \
        .reshape(channel_data.width, channel_data.height)

    img_demosaiced = pa.demosaicing(channel_to_polarize_array)

    angles = np.deg2rad([0, 45, 90, 135])
    img_stokes = pa.calcStokes(img_demosaiced, angles)

    if conversion_type == ConversionTypeEnum.INTENSITY:
        result_channel_df = pd.DataFrame(data=np.round(pa.cvtStokesToIntensity(img_stokes), 0).astype(np.uint8)
                                         .astype("str").astype(decimal.Decimal).flatten())
        result_channel_names = [CONVERTED_CHANNEL_INTENSITY_NAME_TEMPLATE + channel_name]
    elif conversion_type == ConversionTypeEnum.DOLP:
        result_channel_df = pd.DataFrame(data=np.round(pa.cvtStokesToDoLP(img_stokes), 0).astype(np.uint8)
                                         .astype("str").astype(decimal.Decimal).flatten())
        result_channel_names = [CONVERTED_CHANNEL_DOLP_NAME_TEMPLATE + channel_name]
    elif conversion_type == ConversionTypeEnum.AOLP:
        # HSV
        img_aolp = pa.cvtStokesToAoLP(img_stokes)
        aolp_hsv_matrix = pa.applyColorToAoLP(img_aolp).astype("str").astype(decimal.Decimal)
        aolp_channels_array = aolp_hsv_matrix.reshape(-1, aolp_hsv_matrix.shape[2])

        img_dolp = pa.cvtStokesToDoLP(img_stokes)

        # AoLP_light - DoLP applied as saturation
        img_AoLP_light = pa.applyColorToAoLP(img_aolp, saturation=img_dolp).astype("str").astype(decimal.Decimal)
        aolp_channels_array = np.append(aolp_channels_array, img_AoLP_light
                                        .reshape(-1, img_AoLP_light.shape[2]), axis=1)

        # AoLP_dark - DoLP applied as value
        img_AoLP_dark = pa.applyColorToAoLP(img_aolp, value=img_dolp).astype("str").astype(decimal.Decimal)
        aolp_channels_array = np.append(aolp_channels_array, img_AoLP_dark
                                        .reshape(-1, img_AoLP_light.shape[2]), axis=1)

        result_channel_df = pd.DataFrame(data=aolp_channels_array)
        result_channel_names = [CONVERTED_CHANNEL_AOLP_H_NAME_TEMPLATE + channel_name,
                                CONVERTED_CHANNEL_AOLP_S_NAME_TEMPLATE + channel_name,
                                CONVERTED_CHANNEL_AOLP_V_NAME_TEMPLATE + channel_name,
                                CONVERTED_CHANNEL_AOLP_LIGHT_H_NAME_TEMPLATE + channel_name,
                                CONVERTED_CHANNEL_AOLP_LIGHT_S_NAME_TEMPLATE + channel_name,
                                CONVERTED_CHANNEL_AOLP_LIGHT_V_NAME_TEMPLATE + channel_name,
                                CONVERTED_CHANNEL_AOLP_DARK_H_NAME_TEMPLATE + channel_name,
                                CONVERTED_CHANNEL_AOLP_DARK_S_NAME_TEMPLATE + channel_name,
                                CONVERTED_CHANNEL_AOLP_DARK_V_NAME_TEMPLATE + channel_name
                                ]
    else:
        raise Exception("ERROR: Wrong conversion type!")

    result_channel_df.columns = result_channel_names

    for r_name in result_channel_names:
        converted_channels_data_map.append(ConvertedChannelData(channel_name, r_name, conversion_type))

    return pd.concat([df, result_channel_df], axis=1), converted_channels_data_map
