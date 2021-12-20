from typing import Final


class ChannelData:
    def __init__(self, name: str, bit_size: int,
                 channel_width: int = None, channel_height: int = None):
        self.name: Final = name
        self.bit_size: Final = bit_size
        self.width: Final = channel_width
        self.height: Final = channel_height
