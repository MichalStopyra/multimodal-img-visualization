from typing import Final


class ChannelData:
    def __init__(self, name: str, bit_size: int, max_value: int = None, standarized: bool = False):
        self.name: Final = name
        self.bit_size: Final = bit_size
        self.max_value = max_value
        self.standarized = standarized
