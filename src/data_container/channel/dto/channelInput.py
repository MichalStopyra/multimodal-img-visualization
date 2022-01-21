from abc import ABCMeta

from src.data_container.channel.dto.channelData import ChannelData


class ChannelInputInterface:
    __metaclass__ = ABCMeta

    def __init__(self, channels_names_and_bit_sizes_tuple: [(str, int)]):
        self.channels_names_and_bit_sizes = []
        if isinstance(channels_names_and_bit_sizes_tuple, list):
            for tpl in channels_names_and_bit_sizes_tuple:
                self.channels_names_and_bit_sizes.append(ChannelData(tpl[0], tpl[1]))
        else:
            self.channels_names_and_bit_sizes.append(ChannelData(
                channels_names_and_bit_sizes_tuple[0], channels_names_and_bit_sizes_tuple[1]))


class ChannelInput(ChannelInputInterface):
    def __init__(self, channel_image_path: str, channels_names_and_bit_sizes_tuple: [(str, int)]):
        # order and number is major
        super().__init__(channels_names_and_bit_sizes_tuple)
        self.channel_image_path = channel_image_path


class ChannelInputMock(ChannelInputInterface):
    def __init__(self, channel_name: str, bit_size: int, pixel_values: [float]):
        super().__init__([(channel_name, bit_size)])
        self.pixel_values = pixel_values
