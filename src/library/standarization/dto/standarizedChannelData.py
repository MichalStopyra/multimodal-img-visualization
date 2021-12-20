from typing import Final


class StandarizedChannelData:
    def __init__(self, original_channel_name: str, standarized_channel_name: str, standarization_multiplier: int):
        self.original_channel_name: Final = original_channel_name
        self.standarized_channel_name: Final = standarized_channel_name
        self.standarization_multiplier = standarization_multiplier
