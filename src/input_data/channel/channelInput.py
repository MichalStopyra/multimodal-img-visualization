from abc import ABCMeta

from src.input_data.channel.channelNameAndBitSize import ChannelNameAndBitSize


class ChannelInputInterface:
    __metaclass__ = ABCMeta

    def __init__(self, channel_names: [ChannelNameAndBitSize]):
        self.channels_names_and_bit_sizes = channel_names


class ChannelInput(ChannelInputInterface):
    def __init__(self, channel_image_path: str, channels_names_and_bit_sizes: [ChannelNameAndBitSize]):
        # order and number is major
        super().__init__(channels_names_and_bit_sizes)
        self.channel_image_path = channel_image_path


class ChannelInputMock(ChannelInputInterface):
    def __init__(self, channel_name: str, bit_size: int,  pixel_values: [float]):
        super().__init__([ChannelNameAndBitSize(channel_name, bit_size)])
        self.pixel_values = pixel_values
