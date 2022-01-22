import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.library.conversion._conversionBusinessLogic import _convert_channel
from src.library.conversion.dto.ConvertedChannelData import ConvertedChannelData
from src.library.conversion.enum.conversionTypeEnum import ConversionTypeEnum


class ConversionApi:
    @staticmethod
    def convert_channel(df: pd.DataFrame, channels_data_map: [ChannelData],
                        channel_name: str, conversion_type: ConversionTypeEnum,
                        converted_channels_data_map: [ConvertedChannelData]) -> (pd.DataFrame, [ConvertedChannelData]):
        return _convert_channel(df, channels_data_map, channel_name, conversion_type, converted_channels_data_map)
