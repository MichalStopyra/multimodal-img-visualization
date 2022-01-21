import decimal

import numpy as np
import numpy as np
import pandas as pd
import polanalyser as pa

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelData import ChannelData
from src.library.conversion.dto.ConvertedChannelData import ConvertedChannelData
from src.library.conversion.enum.conversionTypeEnum import ConversionTypeEnum
from src.library.properties.properties import CONVERTED_CHANNEL_INTENSITY_NAME_TEMPLATE, \
    CONVERTED_CHANNEL_DOLP_NAME_TEMPLATE, CONVERTED_CHANNEL_AOLP_NAME_TEMPLATE


def _convert_channel(df: pd.DataFrame, channels_data_map: [ChannelData],
                     channel_name: str, conversion_type: ConversionTypeEnum,
                     converted_channels_data_map: [ConvertedChannelData]) -> (pd.DataFrame, [ConvertedChannelData]):
    channel_data = ChannelApi.find_channel_by_name(channels_data_map, channel_name)

    channel_to_polarize_array = df[channel_name].to_numpy().astype(np.uint8) \
        .reshape(channel_data.width, channel_data.height)

    img_demosaiced = pa.demosaicing(channel_to_polarize_array)

    angles = np.deg2rad([0, 45, 90, 135])
    img_stokes = pa.calcStokes(img_demosaiced, angles)

    if conversion_type == ConversionTypeEnum.INTENSITY:
        result_channel_df = pd.DataFrame(data=np.round(pa.cvtStokesToIntensity(img_stokes), 0).astype(np.uint8)
                                         .astype("str").astype(decimal.Decimal).flatten())
        result_channel_name = CONVERTED_CHANNEL_INTENSITY_NAME_TEMPLATE + channel_name
    elif conversion_type == ConversionTypeEnum.DOLP:
        result_channel_df = pd.DataFrame(data=np.round(pa.cvtStokesToDoLP(img_stokes), 0).astype(np.uint8)
                                         .astype("str").astype(decimal.Decimal).flatten())
        result_channel_name = CONVERTED_CHANNEL_DOLP_NAME_TEMPLATE + channel_name
    elif conversion_type == ConversionTypeEnum.AOLP:
        result_channel_df = pd.DataFrame(data=np.round(pa.cvtStokesToAoLP(img_stokes), 0).astype(np.uint8)
                                         .astype("str").astype(decimal.Decimal).flatten())
        result_channel_name = CONVERTED_CHANNEL_AOLP_NAME_TEMPLATE + channel_name
    else:
        raise Exception("ERROR: Wrong conversion type!")

    result_channel_df.columns = [result_channel_name]

    converted_channels_data_map.append(ConvertedChannelData(channel_name, result_channel_name, conversion_type))
    return pd.concat([df, result_channel_df], axis=1), converted_channels_data_map
