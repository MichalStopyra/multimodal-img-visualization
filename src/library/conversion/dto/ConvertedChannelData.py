from typing import Final

from src.library.conversion.enum.conversionTypeEnum import ConversionTypeEnum


class ConvertedChannelData:
    def __init__(self, initial_channel_name: str, converted_channel_name: str, conversion_type: ConversionTypeEnum):
        self.initial_channel_name: Final = initial_channel_name
        self.converted_channel_name: Final = converted_channel_name
        self.conversion_type = conversion_type
