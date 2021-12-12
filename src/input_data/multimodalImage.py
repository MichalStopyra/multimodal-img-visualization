import cv2

from src.input_data.channel.channelInput import ChannelInputInterface, ChannelInput, ChannelInputMock
from src.utils.utils import *


def load_and_convert_mat_to_df(channels_inputs: [ChannelInputInterface]) -> (pd.DataFrame, [ChannelNameAndBitSize]):
    ready_channels = []
    for channel in channels_inputs:
        if isinstance(channel, ChannelInput):
            input_mat = cv2.cvtColor(cv2.imread(channel.channel_image_path), cv2.COLOR_BGR2RGB)
        elif isinstance(channel, ChannelInputMock):
            # TODO: mock pixel values
            input_mat = channel.pixel_values
        else:
            raise Exception("Channel input is of wrong type")

        ready_channels.append(ReadyChannel(input_mat, channel.channels_names_and_bit_sizes))

    return ready_channels_to_df(ready_channels)


class MultimodalImage:
    # class used for creating multimodal images from multi input images
    def __init__(self, channels_inputs: [ChannelInputInterface]):
        self.input_df, self.channels_name_bit_size_map = load_and_convert_mat_to_df(channels_inputs)
