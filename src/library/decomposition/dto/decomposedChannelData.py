from typing import Final


class DecomposedChannelData:
    def __init__(self, initial_channel_name: str, decomposition_object,
                 decomposed_channel_name: str, from_standarized_channel: bool):
        self.initial_channel_name: Final = initial_channel_name
        self.decomposed_channel_name: Final = decomposed_channel_name
        self.decomposition_object = decomposition_object
        self.from_standarized_channel = from_standarized_channel


