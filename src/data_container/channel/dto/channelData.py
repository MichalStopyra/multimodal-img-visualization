from typing import Final


class ChannelData:
    def __init__(self, name: str, bit_size: int,
                 channel_width: int = None, channel_height: int = None,
                 max_value: int = None, standarized: bool = False):
        self.name: Final = name
        self.bit_size: Final = bit_size
        self.width: Final = channel_width
        self.height: Final = channel_height
        self.max_value = max_value
        self.standarized = standarized
