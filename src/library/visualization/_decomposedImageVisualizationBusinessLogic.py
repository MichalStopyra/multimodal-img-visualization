import cv2
import matplotlib
import numpy as np
import pandas as pd

from src.data_container.decomposed_image.decomposedImage import DecomposedImage
from src.library.properties.properties import STD_MAX_PIXEL_VALUE
from src.library.visualization._channelValidationBusinessLogic import _validate_channel_indexes, \
    _validate_number_of_channels_for_decomposed_image_channels, _validate_if_channels_standarized
from src.library.visualization._visualizationBusinessLogic import _save_img
from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum


def _decomposed_image_channels_df_to_image_save_file(decomposed_image_data: DecomposedImage,
                                                     output_name: str,
                                                     output_width: int, output_height: int,
                                                     output_format: OutputImageFormatEnum,
                                                     visualization_channels_type: VisualizationChannelsEnum,
                                                     component_numbers_as_channels: [int]):
    _validate_channel_indexes(component_numbers_as_channels, decomposed_image_data.decomposed_image_df)

    _validate_number_of_channels_for_decomposed_image_channels(visualization_channels_type,
                                                               len(component_numbers_as_channels))

    _validate_if_channels_standarized(visualization_channels_type, decomposed_image_data.image_standarized)

    if visualization_channels_type == VisualizationChannelsEnum.HSV:
        channel_1, channel_2, channel_3 = __hsv_prepare_channels(decomposed_image_data.decomposed_image_df,
                                                                 component_numbers_as_channels, output_width,
                                                                 output_height)
        result_array = np.round(matplotlib.colors.rgb_to_hsv(cv2.merge((channel_1, channel_2, channel_3)))
                                * STD_MAX_PIXEL_VALUE, 0).astype(np.uint8)

    elif visualization_channels_type == VisualizationChannelsEnum.GRAY_SCALE:
        result_array = np.reshape(decomposed_image_data.decomposed_image_df.iloc[:, component_numbers_as_channels[0]]
                                  .to_numpy().astype(np.uint8), (output_width, output_height))

    elif visualization_channels_type == VisualizationChannelsEnum.RGB:
        channel_1, channel_2, channel_3 = __rgb_prepare_channels(decomposed_image_data.decomposed_image_df,
                                                                 component_numbers_as_channels, output_width,
                                                                 output_height)

        result_array = cv2.merge((channel_1, channel_2, channel_3))

    else:
        raise Exception("Error - Wrong Visualization Type")

    _save_img(result_array, output_name, output_format)


def _decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file(decomposed_rvrs_dcmpsd_image_df: pd.DataFrame,
                                                                 output_name: str,
                                                                 output_width: int, output_height: int,
                                                                 output_format: OutputImageFormatEnum,
                                                                 visualization_channels_type: VisualizationChannelsEnum,
                                                                 component_numbers_as_channels: [int]):
    _validate_channel_indexes(component_numbers_as_channels, decomposed_rvrs_dcmpsd_image_df)

    _validate_number_of_channels_for_decomposed_image_channels(visualization_channels_type,
                                                               len(component_numbers_as_channels))

    if visualization_channels_type == VisualizationChannelsEnum.HSV:
        raise Exception("Cannot display hsv image after reverse decomposition on whole image!")
    elif visualization_channels_type == VisualizationChannelsEnum.GRAY_SCALE:
        result_array = np.reshape(decomposed_rvrs_dcmpsd_image_df.iloc[:, component_numbers_as_channels[0]]
                                  .astype(float).to_numpy().astype(np.uint8), (output_width, output_height))

    elif visualization_channels_type == VisualizationChannelsEnum.RGB:
        channel_1, channel_2, channel_3 = __rgb_prepare_channels(decomposed_rvrs_dcmpsd_image_df,
                                                                 component_numbers_as_channels, output_width,
                                                                 output_height)

        result_array = cv2.merge((channel_1, channel_2, channel_3))

    else:
        raise Exception("Error - Wrong Visualization Type")

    _save_img(result_array, output_name, output_format)


def __hsv_prepare_channels(df: pd.DataFrame, component_numbers_as_channels: [int],
                           output_width: int, output_height: int):
    return np.reshape(df.iloc[:, component_numbers_as_channels[0] - 1].to_numpy(),
                      (output_width, output_height)).astype(float), \
           np.reshape(df.iloc[:, component_numbers_as_channels[1] - 1].to_numpy(),
                      (output_width, output_height)).astype(float), \
           np.reshape(df.iloc[:, component_numbers_as_channels[2] - 1].to_numpy(),
                      (output_width, output_height)).astype(float)


def __rgb_prepare_channels(df: pd.DataFrame, component_numbers_as_channels: [int],
                           output_width: int, output_height: int):
    return np.reshape(df.iloc[:, component_numbers_as_channels[0] - 1].to_numpy(),
                      (output_width, output_height)).astype(float).astype(np.uint8), \
           np.reshape(df.iloc[:, component_numbers_as_channels[1] - 1].to_numpy(),
                      (output_width, output_height)).astype(float).astype(np.uint8), \
           np.reshape(df.iloc[:, component_numbers_as_channels[2] - 1].to_numpy(),
                      (output_width, output_height)).astype(float).astype(np.uint8)
