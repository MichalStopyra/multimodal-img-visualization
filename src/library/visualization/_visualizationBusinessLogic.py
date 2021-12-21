import os

import cv2
import cv2.cv2
import matplotlib
import numpy as np
import pandas as pd
from PIL import Image as im

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelData import ChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.properties.properties import OUTPUT_IMAGE_PATH, STD_MAX_PIXEL_VALUE
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData
from src.library.standarization.standarizationApi import StandarizationApi
from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum, translate_output_format_enum
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum


def _df_to_image_and_save(df: pd.DataFrame, channel_data_map: [ChannelData],
                          output_name: str, output_width: int, output_height: int, output_format: OutputImageFormatEnum,
                          visualization_channels_type: VisualizationChannelsEnum,
                          std_channels_data_map: [StandarizedChannelData],
                          rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData],
                          channel_name_1: str = None, channel_name_2: str = None, channel_name_3: str = None):
    __raise_exception_if_empty_df_or_wrong_channel_names(df, channel_name_1, channel_name_2, channel_name_3)

    if visualization_channels_type == VisualizationChannelsEnum.HSV:
        channel_1, channel_2, channel_3 = __check_and_find_channels_for_hsv(df,
                                                                            output_width, output_height,
                                                                            std_channels_data_map,
                                                                            rvrs_decomposed_channels_data_map,
                                                                            channel_name_1,
                                                                            channel_name_2, channel_name_3)
        result_array = np.round(matplotlib.colors.rgb_to_hsv(cv2.merge((channel_1, channel_2, channel_3)))
                                * STD_MAX_PIXEL_VALUE, 0) \
            .astype(np.uint8)

    elif visualization_channels_type == VisualizationChannelsEnum.GRAY_SCALE:
        __validate_gray_scale_channels(channel_name_1, channel_name_2, channel_name_3,
                                       rvrs_decomposed_channels_data_map, std_channels_data_map)

        result_array = np.reshape(df[channel_name_1].to_numpy().astype(np.uint8), (output_width, output_height))

    elif visualization_channels_type == VisualizationChannelsEnum.RGB:
        __validate_rgb_channels(channel_name_1, channel_name_2, channel_name_3, rvrs_decomposed_channels_data_map,
                                std_channels_data_map)

        channel_1, channel_2, channel_3 = \
            __reshape_channels_to_channel_image_arrays(df, channel_name_1, channel_name_2, channel_name_3,
                                                       output_width, output_height)

        result_array = cv2.merge((channel_1, channel_2, channel_3))

    else:
        raise Exception("Error - Wrong Visualization Type")

    _save_img(result_array, output_name, output_format)


def __validate_gray_scale_channels(channel_name_1, channel_name_2, channel_name_3, rvrs_decomposed_channels_data_map,
                                   std_channels_data_map):
    if not channel_name_1:
        raise Exception("ERROR: In order to produce gray scale image, channel_1 needs to be specified!")
    if channel_name_2 or channel_name_3:
        print("WARNING: Gray scale image chosen - channels 2 and 3 will be omitted")
    if __is_given_channel_of_standarized_type(channel_name_1, std_channels_data_map,
                                              rvrs_decomposed_channels_data_map):
        print("WARNING: Gray scale image chosen - provided standarized channel! Output will not make any sense!")


def __validate_rgb_channels(channel_name_1, channel_name_2, channel_name_3, rvrs_decomposed_channels_data_map,
                            std_channels_data_map):
    if not channel_name_1 or not channel_name_2 or not channel_name_3:
        raise Exception('ERROR - In order to create hsv image - pass 3 channel names!')

    for channel_name in [channel_name_1, channel_name_2, channel_name_3]:
        if __is_given_channel_of_standarized_type(channel_name, std_channels_data_map,
                                                  rvrs_decomposed_channels_data_map):
            print("WARNING: RGB image chosen - channel ", channel_name, " is standarized!")


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

    channel_1 = StandarizationApi.destandarize_channel_array(
        np.reshape(df[channel_name_1].to_numpy().astype(float), (output_width, output_height)),
        ChannelApi.find_channel_by_name(channel_data_map, channel_name_1)) \
        if channel_name_1 else np.zeros((output_width, output_height)).astype(np.uint8)

    channel_2 = StandarizationApi.destandarize_channel_array(
        np.reshape(df[channel_name_2].to_numpy().astype(float), (output_width, output_height)),
        ChannelApi.find_channel_by_name(channel_data_map, channel_name_2)) \
        if channel_name_2 else np.zeros((output_width, output_height)).astype(np.uint8)

    channel_3 = StandarizationApi.destandarize_channel_array(
        np.reshape(df[channel_name_3].to_numpy().astype(float), (output_width, output_height)),
        ChannelApi.find_channel_by_name(channel_data_map, channel_name_3)) \
        if channel_name_3 else np.zeros((output_width, output_height)).astype(np.uint8)

    return channel_1, channel_2, channel_3


def __check_and_find_channels_for_hsv(df: pd.DataFrame,
                                      output_width: int, output_height: int,
                                      std_channel_data_map: [StandarizedChannelData],
                                      rvrs_decomposed_channel_data_map: [ReverseDecomposedChannelData],
                                      channel_name_1: str, channel_name_2: str, channel_name_3: str
                                      ) -> (np.ndarray, np.ndarray, np.ndarray):
    if not channel_name_1 or not channel_name_2 or not channel_name_3:
        raise Exception('ERROR - In order to create hsv image - pass 3 channel names!')

    __raise_exception_if_channels_not_standarized([channel_name_1, channel_name_2, channel_name_3],
                                                  std_channel_data_map, rvrs_decomposed_channel_data_map)

    return np.reshape(df[channel_name_1].to_numpy(), (output_width, output_height)).astype(float), \
           np.reshape(df[channel_name_2].to_numpy(), (output_width, output_height)).astype(float), \
           np.reshape(df[channel_name_3].to_numpy(), (output_width, output_height)).astype(float)


def __reshape_channels_to_channel_image_arrays(df: pd.DataFrame,
                                               channel_name_1: str, channel_name_2: str, channel_name_3: str,
                                               output_width: int, output_height: int
                                               ) -> (np.ndarray, np.ndarray, np.ndarray):
    return np.reshape(df[channel_name_1].to_numpy(), (output_width, output_height)).astype(float).astype(np.uint8), \
           np.reshape(df[channel_name_2].to_numpy(), (output_width, output_height)).astype(float).astype(np.uint8), \
           np.reshape(df[channel_name_3].to_numpy(), (output_width, output_height)).astype(float).astype(np.uint8)


def __raise_exception_if_channels_not_standarized(channel_names_list: [ChannelData],
                                                  std_channels_data_map: [StandarizedChannelData],
                                                  rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData]):
    for channel_name in channel_names_list:
        if not __is_given_channel_of_standarized_type(channel_name, std_channels_data_map,
                                                      rvrs_decomposed_channels_data_map):
            raise Exception("Error: HSV image requires standarized channels data!")


def __raise_exception_if_empty_df_or_wrong_channel_names(df: pd.DataFrame,
                                                         channel_name_1: str, channel_name_2: str, channel_name_3: str):
    if df is None or df.empty:
        raise Exception("Error - chosen df does not exist - check if correct method has been chosen")

    if (channel_name_1 and not channel_name_1 in df.columns) \
            or (channel_name_2 and not channel_name_2 in df.columns) \
            or (channel_name_3 and not channel_name_3 in df.columns):
        raise Exception("Error - chosen channels do not exist in the image")


def __check_decomposed_df_size(df: pd.DataFrame, visualization_channels_type: VisualizationChannelsEnum):
    if visualization_channels_type in (VisualizationChannelsEnum.RGB, VisualizationChannelsEnum.HSV) \
            and len(df.columns) < 3:
        raise Exception("Error - creating a 3 channel image requires at least 3 channels' df")


def __is_given_channel_of_standarized_type(channel_name: str, std_channels_data_map: [StandarizedChannelData],
                                           rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData]
                                           ) -> bool:
    std_map_element_list = list(filter(
        lambda channel: channel.standarized_channel_name == channel_name, std_channels_data_map))

    rvrs_decomposed_map_standarized_element_list = list(filter(
        lambda channel: channel.rvrs_decomposed_channel_name == channel_name and channel.from_standarized_channel,
        rvrs_decomposed_channels_data_map))

    return (std_map_element_list is not None and len(std_map_element_list) != 0) \
           or (rvrs_decomposed_map_standarized_element_list is not None
               and len(rvrs_decomposed_map_standarized_element_list) != 0)
