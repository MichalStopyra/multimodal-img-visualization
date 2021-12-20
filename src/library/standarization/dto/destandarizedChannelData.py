from typing import Final


class DestandarizedChannelData:
    def __init__(self, original_channel_name: str, destandarized_channel_name: str):
        self.original_channel_name: Final = original_channel_name
        self.destandarized_channel_name: Final = destandarized_channel_name
