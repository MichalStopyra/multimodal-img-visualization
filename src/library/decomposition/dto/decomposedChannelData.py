from typing import Final


class DecomposedChannelData:
    def __init__(self, original_channel_name: str, decomposition_object):
        self.original_channel_name: Final = original_channel_name
        self.decomposition_object = decomposition_object


