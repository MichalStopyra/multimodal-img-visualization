from typing import Dict

import numpy as np
import pandas as pd

from src.data_container.channel.dto.channelInput import ChannelInputInterface
from src.data_container.dataContainer import DataContainer
from src.library.decomposition.decompositionApi import DecompositionApi
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.standarization.enum.standarizationModeEnum import StandarizationModeEnum
from src.library.standarization.standarizationApi import StandarizationApi
from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum
from src.library.visualization.visualizationApi import VisualizationApi


# ------------------------- MAIN LIBRARY API METHODS--------------------------------------


def load_new_multimodal_image_from_input(data_container: DataContainer,
                                         channels_inputs: [ChannelInputInterface]):
    """
          load_multimodal_image_from_input loads multimodal image into data_container
          It is possible to load it from a group of files containing different channels data
          Another way is to add it using np.ndarray
    """

    data_container.load_multimodal_image_from_input(channels_inputs)


def add_channels_to_multimodal_img(data_container: DataContainer,
                                   channels_inputs: [ChannelInputInterface]):
    """
    add_channels_to_multimodal_img provides a functionality to add a new channel (or multimple channels simultaneously)
        to a multimodal image. When the image has not been created yet, it generates one and adds chosen channels.

        1. channel_inputs contain following information:
            - image channel path : str
            - channel name : str
            - a max bit size of the channel : int
    """

    data_container.add_channels_to_multimodal_img(channels_inputs)


def standarize_image_channels(data_container: DataContainer,
                              channels_to_exclude: [str],
                              standarization_modes: Dict[str, StandarizationModeEnum] = None):
    """
        standarize_image_channels method standarizes multimodal image channels

        1. Adding a channel to channels_to_exclude array excludes chosen channels from global standarization.
        2. standarization_modes is a key -> value map where channel names are
            the keys and standarization_modes are the values.
        3. Possible standarization_modes:
            - max & min values are the actual max & min pixel values of a channel.
            - max value is the max bit size of the channel and min value is 0.
    """

    data_container.multimodal_image.image_df, data_container.standarized_channels_data_map = \
        StandarizationApi.standarize_image_channels(data_container.get_image_df(), channels_to_exclude,
                                                    data_container.get_channels_data_map(),
                                                    data_container.standarized_channels_data_map,
                                                    standarization_modes)


def destandarize_channel_by_name(data_container: DataContainer, initial_channel_name: str,
                                 after_reverse_decomposition: bool):
    """
        destandarize_channel_by_name method destandarizes multimodal image channels according to the way it was standarized
    """

    data_container.multimodal_image.image_df, data_container.destandarized_channels_data_map = \
        StandarizationApi.destandarize_channel(data_container.get_image_df(), initial_channel_name,
                                               after_reverse_decomposition,
                                               data_container.standarized_channels_data_map,
                                               data_container.destandarized_channels_data_map,
                                               data_container.rvrs_decomposed_channels_data_map)


def multimodal_image_df_to_image_save_file(data_container: DataContainer,
                                           output_name: str, output_width: int, output_height: int,
                                           output_format: OutputImageFormatEnum,
                                           visualization_channels_type: VisualizationChannelsEnum,
                                           channel_name_1: str = None, channel_name_2: str = None,
                                           channel_name_3: str = None):
    """
         multimodal_image_df_to_image_save_file creates an image from multimodal image df and saves it to file
         It can create an RGB, HSV or GrayScale image depending on given arguments
    """

    VisualizationApi.df_to_image_and_save(data_container.get_image_df(),
                                          output_name, output_width, output_height, output_format,
                                          visualization_channels_type,
                                          data_container.standarized_channels_data_map,
                                          data_container.decomposed_channels_data_map,
                                          data_container.rvrs_decomposed_channels_data_map,
                                          channel_name_1, channel_name_2, channel_name_3)


def decomposed_image_channels_df_to_image_save_file(data_container: DataContainer,
                                                    output_name: str, output_width: int, output_height: int,
                                                    output_format: OutputImageFormatEnum,
                                                    visualization_channels_type: VisualizationChannelsEnum,
                                                    component_numbers_as_channels: [int]):
    """
         decomposed_image_channels_df_to_image_save_file creates an image from decomposed image (decomposed channels)
         It can create an RGB, HSV or GrayScale image depending on given arguments
    """

    VisualizationApi.decomposed_image_channels_df_to_image_save_file(data_container.decomposed_image_data,
                                                                     output_name, output_width, output_height,
                                                                     output_format,
                                                                     visualization_channels_type,
                                                                     component_numbers_as_channels)


def decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file(data_container: DataContainer,
                                                                output_name: str, output_width: int, output_height: int,
                                                                output_format: OutputImageFormatEnum,
                                                                visualization_channels_type: VisualizationChannelsEnum,
                                                                component_numbers_as_channels: [int]):
    """
    TODO:
         decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file creates an image from decomposed image (decomposed channels)
         It can create an RGB, HSV or GrayScale image depending on given arguments
    """

    VisualizationApi.decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file(
        data_container.decomposed_rvrs_dcmpsd_image_df,
        output_name, output_width, output_height,
        output_format,
        visualization_channels_type,
        component_numbers_as_channels)


def save_image_to_file(image_array: np.ndarray, image_name: str, image_format: OutputImageFormatEnum):
    """
            save_image_to_file saves an image from (np.ndarray) image_array to file
    """

    VisualizationApi.save_img(image_array, image_name, image_format)


def decompose_channel_resolution_wrapper(data_container: DataContainer, channel_name: str,
                                         decomposition_type: DecompositionEnum, take_standarized_channel: bool,
                                         fast_ica_n_components=None) -> (pd.DataFrame, [DecomposedChannelData]):
    """
           decompose_channel_wrapper transforms a chosen channel using chosen decomposition type - PCA, FastICA, NMF
    """

    data_container.multimodal_image.image_df, data_container.decomposed_channels_data_map = \
        DecompositionApi.decompose_channel_resolution_wrapper(data_container.get_image_df(),
                                                              data_container.get_channels_data_map(),
                                                              data_container.decomposed_channels_data_map,
                                                              data_container.standarized_channels_data_map,
                                                              channel_name,
                                                              decomposition_type, take_standarized_channel,
                                                              fast_ica_n_components)


def decompose_image_channels_wrapper(data_container: DataContainer, decomposition_type: DecompositionEnum,
                                     channel_names_and_take_std_tuple: [(str, bool)],
                                     fast_ica_n_components=None):
    """
           decompose_image_channels_wrapper transforms a whole multimodal image using chosen decomposition type - PCA, FastICA, NMF
           as a result image consisting of fewer channels is returned
    """

    data_container.decomposed_image_data = \
        DecompositionApi.decompose_image_channels_wrapper(data_container.get_image_df(), decomposition_type,
                                                          channel_names_and_take_std_tuple,
                                                          data_container.standarized_channels_data_map,
                                                          fast_ica_n_components)


def rvrs_decompose_image_channels(data_container: DataContainer):
    """
           TODO
    """
    data_container.decomposed_rvrs_dcmpsd_image_df = DecompositionApi.rvrs_decompose_image_channels(
        data_container.decomposed_image_data)


def reverse_decompose_channel(data_container: DataContainer, channel_name: str
                              ) -> (pd.DataFrame, [ReverseDecomposedChannelData]):
    data_container.multimodal_image.image_df, data_container.rvrs_decomposed_channels_data_map = \
        DecompositionApi.reverse_decompose_channel(data_container.get_image_df(), channel_name,
                                                   data_container.decomposed_channels_data_map,
                                                   data_container.rvrs_decomposed_channels_data_map)

# -----------------------------------------------------------------------------
