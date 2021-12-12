import logging

import PIL.Image
import cv2.cv2
import matplotlib
import numpy as np
import pandas as pd
from PIL import Image as im

from src.input_data.channel.channelData import ChannelData, find_channel_by_name
from src.output_data.outputChannelsEnum import OutputChannelsEnum
from src.output_data.outputFormatEnum import OutputFormatEnum, translate_output_format_enum
from src.utils.constants import OUTPUT_IMAGE_PATH, STD_MAX_PIXEL_VALUE
import os
import cv2


def df_to_image(df: pd.DataFrame, channel_data_map: [ChannelData], output_name: str,
                output_width: int, output_height: int, output_format: OutputFormatEnum,
                output_channels_type: OutputChannelsEnum,
                channel_name_1: str = None, channel_name_2: str = None, channel_name_3: str = None):
    if output_channels_type == OutputChannelsEnum.HSV:
        channel_1, channel_2, channel_3 = _check_and_find_channels_for_hsv(df, channel_data_map, channel_name_1,
                                                                           channel_name_2, channel_name_3,
                                                                           output_width, output_height)
        result_array = np.round(matplotlib.colors.rgb_to_hsv(cv2.merge((channel_1, channel_2, channel_3)))
                                * STD_MAX_PIXEL_VALUE, 0) \
            .astype(np.uint8)

    else:
        channel_1, channel_2, channel_3 = _df_to_separate_channels_arrays(df, output_width, output_height,
                                                                          channel_data_map,
                                                                          channel_name_1, channel_name_2,
                                                                          channel_name_3)

        if output_channels_type == OutputChannelsEnum.GRAY_SCALE:
            if not channel_name_1:
                raise Exception("ERROR: In order to produce gray scale image, channel_1 needs to be specified!")

            if channel_name_2 or channel_name_3:
                print("Gray scale image chosen - channels 2 and 3 will be omitted")
            result_array = channel_1
        else:
            result_array = cv2.merge((channel_1, channel_2, channel_3))

    save_img(result_array, output_name, output_format)


def save_img(image_array: np.ndarray, image_name: str, image_format: OutputFormatEnum):
    if not os.path.exists(OUTPUT_IMAGE_PATH):
        os.mkdir(OUTPUT_IMAGE_PATH)

    img = im.fromarray(image_array)
    img.save(OUTPUT_IMAGE_PATH + image_name + translate_output_format_enum(image_format))


def _df_to_separate_channels_arrays(df, output_width, output_height, channel_data_map: [ChannelData],
                                    channel_name_1: str, channel_name_2: str = None, channel_name_3: str = None) \
        -> (np.ndarray, np.ndarray, np.ndarray):
    if not channel_name_1 and not channel_name_2 and not channel_name_3:
        raise Exception("ERROR: No channels specified for displaying")

    channel_1 = _destandarize_channel(np.reshape(df[channel_name_1].to_numpy(), (output_width, output_height)),
                                      find_channel_by_name(channel_data_map, channel_name_1)) \
        if channel_name_1 else np.zeros((output_width, output_height)).astype(np.uint8)

    channel_2 = _destandarize_channel(np.reshape(df[channel_name_2].to_numpy(), (output_width, output_height)),
                                      find_channel_by_name(channel_data_map, channel_name_2)) \
        if channel_name_2 else np.zeros((output_width, output_height)).astype(np.uint8)

    channel_3 = _destandarize_channel(np.reshape(df[channel_name_3].to_numpy(), (output_width, output_height)),
                                      find_channel_by_name(channel_data_map, channel_name_3)) \
        if channel_name_3 else np.zeros((output_width, output_height)).astype(np.uint8)

    return channel_1, channel_2, channel_3


def _destandarize_channel(channel_array: np.ndarray, channel_data: ChannelData) -> np.ndarray:
    if not channel_data.standarized:
        return channel_array

    max_value_multiplier = channel_data.max_value if channel_data.max_value is not None \
        else np.power(2, channel_data.bit_size) - 1
    return (np.round(channel_array * max_value_multiplier, 0) % max_value_multiplier).astype(np.uint8)


def _check_and_find_channels_for_hsv(df: pd.DataFrame, channel_data_map: [ChannelData],
                                     channel_name_1: str, channel_name_2: str, channel_name_3: str,
                                     output_width: int, output_height: int) \
        -> (np.ndarray, np.ndarray, np.ndarray):
    channel_data_1 = find_channel_by_name(channel_data_map, channel_name_1)
    channel_data_2 = find_channel_by_name(channel_data_map, channel_name_2)
    channel_data_3 = find_channel_by_name(channel_data_map, channel_name_3)

    raise_exception_if_channels_not_standarized([channel_data_1, channel_data_2, channel_data_3])
    return np.reshape(df[channel_name_1].to_numpy(), (output_width, output_height)), \
           np.reshape(df[channel_name_2].to_numpy(), (output_width, output_height)), \
           np.reshape(df[channel_name_3].to_numpy(), (output_width, output_height))


def raise_exception_if_channels_not_standarized(channel_data_list: [ChannelData]):
    for channel_data in channel_data_list:
        if not channel_data.standarized:
            raise Exception("Error - channel: {} is not standarized, cannot perform action", channel_data.name)
