from typing import Final


class ReverseDecomposedChannelData:
    def __init__(self, initial_channel_name: str, rvrs_decomposed_channel_name: str, from_standarized_channel: bool):
        self.initial_channel_name: Final = initial_channel_name
        self.rvrs_decomposed_channel_name: Final = rvrs_decomposed_channel_name
        self.from_standarized_channel = from_standarized_channel
