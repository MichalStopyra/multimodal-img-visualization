import numpy as np

from src.data_container.channel.dto.channelData import ChannelData


class ReadyChannel:
    def __init__(self, image: np.ndarray, channels_names_and_bit_sizes: [ChannelData]):
        self.image = image
        self.channels_names_and_bit_sizes = channels_names_and_bit_sizes
