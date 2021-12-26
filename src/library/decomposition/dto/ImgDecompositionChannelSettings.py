from typing import Final


class ImgDecompositionChannelSettings:

    def __init__(self, initial_channel_name: str, take_standarized_channel: bool):
        self.initial_channel_name: Final = initial_channel_name
        self.take_standarized_channel: Final = take_standarized_channel
