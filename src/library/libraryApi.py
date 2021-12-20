from typing import Dict

import numpy as np

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelInput import ChannelInputInterface
from src.data_container.dataContainer import DataContainer
from src.library.decomposition.decompositionApi import DecompositionApi
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.standarization.enum.standarizationModeEnum import StandarizationModeEnum
from src.library.standarization.standarizationApi import StandarizationApi
from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum
from src.library.visualization.visualizationApi import VisualizationApi


# ------------------------- MAIN LIBRARY API METHODS--------------------------------------


def load_multimodal_image_from_input(data_container: DataContainer,
                                     channels_inputs: [ChannelInputInterface]):
    """
          load_multimodal_image_from_input loads multimodal image into data_container
          It is possible to load it from a group of files containing different channels data
          Another way is to add it using np.ndarray
    """

    data_container.load_multimodal_image_from_input(channels_inputs)


def standarize_image_channels(data_container: DataContainer,
                              channels_to_exclude: [str],
                              standarization_modes: Dict[str, StandarizationModeEnum] = None):
    """
        standarize_image_channels standarizes multimodal image channels
        It is possible to exclude some channels from standarization, adding their names as channels_to_exclude array arg
    """

    data_container.multimodal_image.image_df, data_container.standarized_channels_data_map = \
        StandarizationApi.standarize_image_channels(data_container.get_image_df(), channels_to_exclude,
                                                    data_container.get_channels_data_map(),
                                                    data_container.standarized_channels_data_map,
                                                    standarization_modes)


def destandarize_channel_by_name(data_container: DataContainer, original_channel_name: str):
    """
        destandarize_channel_by_name destandarizes multimodal image channels according to the way it was standarized
    """

    data_container.multimodal_image.image_df, data_container.destandarized_channels_data_map = \
        StandarizationApi.destandarize_channel(data_container.get_image_df(), original_channel_name,
                                               data_container.standarized_channels_data_map,
                                               data_container.destandarized_channels_data_map)


def multimodal_image_df_to_image_save_file(data_container: DataContainer,
                                           output_name: str, output_width: int, output_height: int,
                                           output_format: OutputImageFormatEnum,
                                           output_channels_type: VisualizationChannelsEnum,
                                           channel_name_1: str = None, channel_name_2: str = None,
                                           channel_name_3: str = None):
    """
         multimodal_image_df_to_image_save_file creates an image from multimodal image df and saves it to file
         It can create an RGB, HSV or GrayScale image depending on given arguments
    """

    VisualizationApi.df_to_image_and_save(data_container.get_image_df(),
                                          data_container.get_channels_data_map(),
                                          False,
                                          output_name, output_width, output_height, output_format,
                                          output_channels_type,
                                          channel_name_1, channel_name_2, channel_name_3)


def standarized_multimodal_image_df_to_image_save_file(data_container: DataContainer,
                                                       output_name: str, output_width: int, output_height: int,
                                                       output_format: OutputImageFormatEnum,
                                                       output_channels_type: VisualizationChannelsEnum,
                                                       channel_name_1: str = None, channel_name_2: str = None,
                                                       channel_name_3: str = None):
    """
         standarized multimodal_image_df_to_image_save_file creates an image from multimodal image df and saves it to file
         It can create an RGB, HSV or GrayScale image depending on given arguments
    """

    VisualizationApi.df_to_image_and_save(data_container.standarized_image_df,
                                          data_container.get_channels_data_map(),
                                          True,
                                          output_name, output_width, output_height, output_format,
                                          output_channels_type,
                                          channel_name_1, channel_name_2, channel_name_3)


# def decomposed_multimodal_image_df_to_image_save_file(data_container: DataContainer,
#                                                       output_name: str, output_width: int, output_height: int,
#                                                       output_format: OutputImageFormatEnum,
#                                                       output_channels_type: VisualizationChannelsEnum,
#                                                       channel_name_1: str = None, channel_name_2: str = None,
#                                                       channel_name_3: str = None):
#     """
#          standarized multimodal_image_df_to_image_save_file creates an image from multimodal image df and saves it to file
#          It can create an RGB, HSV or GrayScale image depending on given arguments
#     """
#
#     # TODO: figure out how to print it - for now chosing first three channels
#     VisualizationApi.decomposed_df_to_image_and_save(data_container.decomposed_image_df,
#                                                      data_container.get_channels_data_map(),
#                                                      True,
#                                                      output_name, output_width, output_height, output_format,
#                                                      output_channels_type)


def save_image_to_file(image_array: np.ndarray, image_name: str, image_format: OutputImageFormatEnum):
    """
            save_image_to_file saves an image from (np.ndarray) image_array to file
    """

    VisualizationApi.save_img(image_array, image_name, image_format)


def decompose_channel_wrapper(data_container: DataContainer, channel_name: str,
                              decomposition_type: DecompositionEnum, take_standarized_channel: bool,
                              fast_ica_n_components=None):
    """
           decompose_channel_wrapper transforms a chosen channel using chosen decomposition type - PCA, FastICA, NMF
    """

    data_container.multimodal_image.image_df, data_container.decomposed_channels_data_map = \
        DecompositionApi.decompose_channel_wrapper(data_container.get_image_df(),
                                                   data_container.get_channels_data_map(),
                                                   data_container.decomposed_channels_data_map,
                                                   data_container.standarized_channels_data_map,
                                                   channel_name,
                                                   decomposition_type, take_standarized_channel, fast_ica_n_components)


def reverse_decompose_channel(data_container: DataContainer, channel_name: str):
    data_container.multimodal_image.image_df = \
        DecompositionApi.reverse_decompose_channel(data_container.get_image_df(), channel_name,
                                                   data_container.decomposed_channels_data_map)

# -----------------------------------------------------------------------------
