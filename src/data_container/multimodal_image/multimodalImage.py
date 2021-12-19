import cv2
import numpy as np
import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.channel.dto.channelInput import ChannelInputInterface, ChannelInput, ChannelInputMock
from src.data_container.channel.dto.readyChannel import ReadyChannel


class MultimodalImage:

    def __init__(self, channels_inputs: [ChannelInputInterface]):
        self.image_df, self.channels_data_map = self.__load_and_convert_mat_to_df(channels_inputs)

    def __load_and_convert_mat_to_df(self, channels_inputs: [ChannelInputInterface]) \
            -> (pd.DataFrame, [ChannelData]):
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

        return self.__ready_channels_to_df(ready_channels)

    def __ready_channels_to_df(self, channels: [ReadyChannel]) -> (pd.DataFrame, [ChannelData]):
        self.__validate_channel_images(channels)

        first_channels = channels.pop(0)
        channel_names_and_bit_sizes = first_channels.channels_names_and_bit_sizes
        channel_matrix = first_channels.image.reshape(-1, first_channels.image.shape[2])
        for channel in channels:
            channel_matrix = np.append(channel_matrix, channel.image.reshape(-1, channel.image.shape[2]), axis=1)

            for name_and_bit_size in channel.channels_names_and_bit_sizes:
                channel_names_and_bit_sizes.append(name_and_bit_size)

        df = pd.DataFrame(data=channel_matrix)

        df.columns = [f'{channel_names_and_bit_sizes[i - 1].name}' for i in range(1, 1 + channel_matrix.shape[1])]
        return df, channel_names_and_bit_sizes

    @staticmethod
    def __validate_channel_images(channels: []):
        invalid_size_channels = [channel for channel in channels
                                 if channel.image.shape[0] != channels[0].image.shape[0]
                                 or channel.image.shape[1] != channels[0].image.shape[1]]
        # TODO: handle different resolutions
        if invalid_size_channels:
            raise Exception("channel images have different resolution")
