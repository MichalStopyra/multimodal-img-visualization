from typing import Final


class ChannelData:
    def __init__(self, name: str, bit_size: int, max_value: int = None, standarized: bool = False):
        self.name: Final = name
        self.bit_size: Final = bit_size
        self.max_value = max_value
        self.standarized = standarized


def find_channel_by_name(channel_data_map: [ChannelData], name: str) -> ChannelData:
    map_element = list(filter(lambda cdm: cdm.name == name, channel_data_map))
    if not map_element or len(map_element) != 1:
        raise Exception("Channel: {}'s data not specified", name)

    return map_element[0]
