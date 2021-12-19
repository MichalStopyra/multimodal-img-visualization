from abc import ABCMeta

from src.data_container.channel.dto.channelData import ChannelData


class ChannelInputInterface:
    __metaclass__ = ABCMeta

    def __init__(self, channel_names: [ChannelData]):
        self.channels_names_and_bit_sizes = channel_names


class ChannelInput(ChannelInputInterface):
    def __init__(self, channel_image_path: str, channels_names_and_bit_sizes: [ChannelData]):
        # order and number is major
        super().__init__(channels_names_and_bit_sizes)
        self.channel_image_path = channel_image_path


class ChannelInputMock(ChannelInputInterface):
    def __init__(self, channel_name: str, bit_size: int, pixel_values: [float]):
        super().__init__([ChannelData(channel_name, bit_size)])
        self.pixel_values = pixel_values
