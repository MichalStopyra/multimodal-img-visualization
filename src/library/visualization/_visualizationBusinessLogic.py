import os

import cv2
import cv2.cv2
import matplotlib
import numpy as np
import pandas as pd
from PIL import Image as im

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelData import ChannelData
from src.library.properties.properties import OUTPUT_IMAGE_PATH, STD_MAX_PIXEL_VALUE
from src.library.standarization.standarizationApi import StandarizationApi
from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum, translate_output_format_enum
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum


def _df_to_image_and_save(df: pd.DataFrame, channel_data_map: [ChannelData], destandarize: bool,
                          output_name: str, output_width: int, output_height: int, output_format: OutputImageFormatEnum,
                          visualization_channels_type: VisualizationChannelsEnum,
                          channel_name_1: str = None, channel_name_2: str = None, channel_name_3: str = None):
    __raise_exception_if_empty_df(df)

    if visualization_channels_type == VisualizationChannelsEnum.HSV:
        channel_1, channel_2, channel_3 = __check_and_find_channels_for_hsv(df, channel_data_map, channel_name_1,
                                                                            channel_name_2, channel_name_3,
                                                                            output_width, output_height)
        result_array = np.round(matplotlib.colors.rgb_to_hsv(cv2.merge((channel_1, channel_2, channel_3)))
                                * STD_MAX_PIXEL_VALUE, 0) \
            .astype(np.uint8)

    elif visualization_channels_type == VisualizationChannelsEnum.GRAY_SCALE:
        if not channel_name_1:
            raise Exception("ERROR: In order to produce gray scale image, channel_1 needs to be specified!")

        if channel_name_2 or channel_name_3:
            print("Gray scale image chosen - channels 2 and 3 will be omitted")

        result_array = StandarizationApi.destandarize_channel(
            np.reshape(df[channel_name_1].to_numpy().astype(float), (output_width, output_height)),
            ChannelApi.find_channel_by_name(channel_data_map, channel_name_1)) \
            if destandarize \
            else ChannelApi.find_channel_by_name(channel_data_map, channel_name_1)

    elif visualization_channels_type == VisualizationChannelsEnum.RGB:
        channel_1, channel_2, channel_3 = \
            __df_destandarize_and_map_to_separate_channels_arrays(df, output_width, output_height, channel_data_map,
                                                                  channel_name_1, channel_name_2, channel_name_3) \
                if destandarize \
                else __reshape_channels_to_channel_image_arrays(df, channel_name_1, channel_name_2, channel_name_3,
                                                                output_width, output_height)

        result_array = cv2.merge((channel_1, channel_2, channel_3))

    else:
        raise Exception("Error - Wrong Visualization Type")

    _save_img(result_array, output_name, output_format)


def _save_img(image_array: np.ndarray, image_name: str, image_format: OutputImageFormatEnum):
    if not os.path.exists(OUTPUT_IMAGE_PATH):
        os.mkdir(OUTPUT_IMAGE_PATH)

    img = im.fromarray(image_array)
    img.save(OUTPUT_IMAGE_PATH + image_name + translate_output_format_enum(image_format))


# def _decomposed_df_to_image_and_save(df: pd.DataFrame, channel_data_map: [ChannelData], destandarize: bool,
#                                      output_name: str, output_width: int, output_height: int,
#                                      output_format: OutputImageFormatEnum,
#                                      visualization_channels_type: VisualizationChannelsEnum):
#     __raise_exception_if_empty_df(df)
#     __check_decomposed_df_size(df, visualization_channels_type)
#     channel_name_1 = df.columns[0]
#
#     channel_name_2, channel_name_3 = (df.columns[1], df.columns[2]) \
#         if visualization_channels_type != VisualizationChannelsEnum.GRAY_SCALE \
#         else (None, None)
#
#     _df_to_image_and_save(df, channel_data_map, destandarize, output_name, output_width, output_height, output_format,
#                           visualization_channels_type, channel_name_1, channel_name_2, channel_name_3)


def __df_destandarize_and_map_to_separate_channels_arrays(df, output_width, output_height,
                                                          channel_data_map: [ChannelData],
                                                          channel_name_1: str, channel_name_2: str = None,
                                                          channel_name_3: str = None
                                                          ) -> (np.ndarray, np.ndarray, np.ndarray):
    if not channel_name_1 and not channel_name_2 and not channel_name_3:
        raise Exception("ERROR: No channels specified for displaying")

    channel_1 = StandarizationApi.destandarize_channel(
        np.reshape(df[channel_name_1].to_numpy().astype(float), (output_width, output_height)),
        ChannelApi.find_channel_by_name(channel_data_map, channel_name_1)) \
        if channel_name_1 else np.zeros((output_width, output_height)).astype(np.uint8)

    channel_2 = StandarizationApi.destandarize_channel(
        np.reshape(df[channel_name_2].to_numpy().astype(float), (output_width, output_height)),
        ChannelApi.find_channel_by_name(channel_data_map, channel_name_2)) \
        if channel_name_2 else np.zeros((output_width, output_height)).astype(np.uint8)

    channel_3 = StandarizationApi.destandarize_channel(
        np.reshape(df[channel_name_3].to_numpy().astype(float), (output_width, output_height)),
        ChannelApi.find_channel_by_name(channel_data_map, channel_name_3)) \
        if channel_name_3 else np.zeros((output_width, output_height)).astype(np.uint8)

    return channel_1, channel_2, channel_3


def __check_and_find_channels_for_hsv(df: pd.DataFrame, channel_data_map: [ChannelData],
                                      channel_name_1: str, channel_name_2: str, channel_name_3: str,
                                      output_width: int, output_height: int) \
        -> (np.ndarray, np.ndarray, np.ndarray):
    channel_data_1 = ChannelApi.find_channel_by_name(channel_data_map, channel_name_1)
    channel_data_2 = ChannelApi.find_channel_by_name(channel_data_map, channel_name_2)
    channel_data_3 = ChannelApi.find_channel_by_name(channel_data_map, channel_name_3)

    __raise_exception_if_channels_not_standarized([channel_data_1, channel_data_2, channel_data_3])

    return np.reshape(df[channel_name_1].to_numpy(), (output_width, output_height)).astype(float), \
           np.reshape(df[channel_name_2].to_numpy(), (output_width, output_height)).astype(float), \
           np.reshape(df[channel_name_3].to_numpy(), (output_width, output_height)).astype(float)


def __reshape_channels_to_channel_image_arrays(df: pd.DataFrame,
                                               channel_name_1: str, channel_name_2: str, channel_name_3: str,
                                               output_width: int, output_height: int
                                               ) -> (np.ndarray, np.ndarray, np.ndarray):
    return np.reshape(df[channel_name_1].to_numpy(), (output_width, output_height)).astype(np.uint8), \
           np.reshape(df[channel_name_2].to_numpy(), (output_width, output_height)).astype(np.uint8), \
           np.reshape(df[channel_name_3].to_numpy(), (output_width, output_height)).astype(np.uint8)


def __raise_exception_if_channels_not_standarized(channel_data_list: [ChannelData]):
    for channel_data in channel_data_list:
        if not channel_data.standarized:
            raise Exception("Error - channel: {} is not standarized, cannot perform action", channel_data.name)


def __raise_exception_if_empty_df(df: pd.DataFrame):
    if df is None or df.empty:
        raise Exception("Error - chosen df does not exist - check if correct method has been chosen")


def __check_decomposed_df_size(df: pd.DataFrame, visualization_channels_type: VisualizationChannelsEnum):
    if visualization_channels_type in (VisualizationChannelsEnum.RGB, VisualizationChannelsEnum.HSV) \
            and len(df.columns) < 3:
        raise Exception("Error - creating a 3 channel image requires at least 3 channels' df")
