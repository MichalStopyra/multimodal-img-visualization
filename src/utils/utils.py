import numpy as np
import pandas as pd

from src.input_data.channel.channelNameAndBitSize import ChannelNameAndBitSize
from src.input_data.channel.readyChannel import ReadyChannel


def array_to_df(input_array: np.array) -> pd.DataFrame:
    new_shape = input_array.reshape(-1, input_array.shape[2])
    df = pd.DataFrame(data=new_shape)
    df.columns = [f'channel{i}' for i in range(1, 1 + new_shape.shape[1])]
    return df


def validate_channel_images(channels: []):
    invalid_size_channels = [channel for channel in channels
                             if channel.image.shape[0] != channels[0].image.shape[0]
                             or channel.image.shape[1] != channels[0].image.shape[1]]
    if invalid_size_channels:
        raise Exception("channel images have different resolution")


def ready_channels_to_df(channels: [ReadyChannel]) -> (pd.DataFrame, [ChannelNameAndBitSize]):
    validate_channel_images(channels)

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
