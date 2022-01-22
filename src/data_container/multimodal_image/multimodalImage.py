import decimal

import cv2
import numpy as np
import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.channel.dto.channelInput import ChannelInputInterface, ChannelInput, ChannelInputFromPixelArray
from src.data_container.channel.dto.readyChannel import ReadyChannel


class MultimodalImage:

    def __init__(self, channels_inputs: [ChannelInputInterface]):
        self.image_df, self.channels_data_map = self.__load_and_convert_mat_to_df(channels_inputs)

    def add_channels_to_multimodal_img(self, channels_inputs: [ChannelInputInterface]):
        image_df_to_concat, channels_data_map_to_append = self.__load_and_convert_mat_to_df(channels_inputs)
        self.image_df = pd.concat([self.image_df, image_df_to_concat], axis=1)
        self.channels_data_map += channels_data_map_to_append

    def __load_and_convert_mat_to_df(self, channels_inputs: [ChannelInputInterface]) \
            -> (pd.DataFrame, [ChannelData]):
        ready_channels = []
        for channel in channels_inputs:
            if isinstance(channel, ChannelInput):
                if len(channel.channels_names_and_bit_sizes) == 1:
                    input_mat = cv2.imread(channel.channel_image_path, cv2.IMREAD_GRAYSCALE)

                elif len(channel.channels_names_and_bit_sizes) == 3:
                    input_mat = cv2.cvtColor(cv2.imread(channel.channel_image_path), cv2.COLOR_BGR2RGB)

                else:
                    raise Exception("ERROR - Wrong amount of channel names and bit sizes!")
            elif isinstance(channel, ChannelInputFromPixelArray):
                input_mat = channel.pixel_values
            else:
                raise Exception("Channel input is of wrong type")

            for channel_data in channel.channels_names_and_bit_sizes:
                channel_data.width = input_mat.shape[0]
                channel_data.height = input_mat.shape[1]

            ready_channels.append(ReadyChannel(input_mat, channel.channels_names_and_bit_sizes))

        return self.__ready_channels_to_df(ready_channels)

    def __ready_channels_to_df(self, channels: [ReadyChannel]) -> (pd.DataFrame, [ChannelData]):
        self.__validate_channel_images(channels)

        first_channels = channels.pop(0)
        channel_names_and_bit_sizes = first_channels.channels_names_and_bit_sizes
        channel_matrix = first_channels.image.reshape(-1, len(channel_names_and_bit_sizes))
        for channel in channels:
            channel_matrix = np.append(channel_matrix, channel.image
                                       .reshape(-1, len(channel.channels_names_and_bit_sizes)), axis=1)

            for name_and_bit_size in channel.channels_names_and_bit_sizes:
                channel_names_and_bit_sizes.append(name_and_bit_size)

        df = pd.DataFrame(data=channel_matrix)

        df.columns = [f'{channel_names_and_bit_sizes[i - 1].name}' for i in range(1, 1 + channel_matrix.shape[1])]

        for column in df.columns:
            df[column] = df[column].astype("string").apply(decimal.Decimal)

        return df, channel_names_and_bit_sizes

    @staticmethod
    def __validate_channel_images(channels: []):
        invalid_size_channels = [channel for channel in channels
                                 if channel.image.shape[0] != channels[0].image.shape[0]
                                 or channel.image.shape[1] != channels[0].image.shape[1]]
        if invalid_size_channels:
            raise Exception("channel images have different resolution")
