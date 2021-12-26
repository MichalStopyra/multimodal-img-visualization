from typing import Final


class DestandarizedChannelData:
    def __init__(self, initial_channel_name: str, destandarized_channel_name: str, after_reverse_decomposition: bool):
        self.initial_channel_name: Final = initial_channel_name
        self.destandarized_channel_name: Final = destandarized_channel_name
        self.after_reverse_decomposition = after_reverse_decomposition
