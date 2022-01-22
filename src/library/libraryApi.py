from typing import Dict

import pandas as pd

from src.data_container.channel.dto.channelInput import ChannelInputInterface
from src.data_container.dataContainer import DataContainer
from src.library.conversion.conversionApi import ConversionApi
from src.library.conversion.enum.conversionTypeEnum import ConversionTypeEnum
from src.library.decomposition.decompositionApi import DecompositionApi
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.standarization.enum.standarizationModeEnum import StandarizationModeEnum
from src.library.standarization.standarizationApi import StandarizationApi
from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum
from src.library.visualization.visualizationApi import VisualizationApi


# ------------------------- MAIN LIBRARY API METHODS--------------------------------------


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

        1. Adding a channel to channels_to_exclude array excludes chosen channels from a global standarization.
        2. standarization_modes is a key -> value dictionary where channel names are
            the keys and standarization_modes are the values.
        3. Possible standarization_modes:
            a) CHANNEL_VALUES_MIN_MAX - max & min values are the actual max & min pixel values of a channel.
            b) BIT_SIZE_MIN_MAX - max value is the max bit size of the channel and min value is 0.
    """

    data_container.multimodal_image.image_df, data_container.standarized_channels_data_map = \
        StandarizationApi.standarize_image_channels(data_container.get_image_df(), channels_to_exclude,
                                                    data_container.get_channels_data_map(),
                                                    data_container.standarized_channels_data_map,
                                                    standarization_modes)


def destandarize_channel_by_name(data_container: DataContainer, initial_channel_name: str,
                                 after_reverse_decomposition: bool):
    """
        destandarize_channel_by_name method destandarizes chosen multimodal image channel according to the way it
            was standarized.

        setting after_reverse_decomposition to True value will destandarize a channel after rvrs_decomposition
    """

    data_container.multimodal_image.image_df, data_container.destandarized_channels_data_map = \
        StandarizationApi.destandarize_channel(data_container.get_image_df(), initial_channel_name,
                                               after_reverse_decomposition,
                                               data_container.standarized_channels_data_map,
                                               data_container.destandarized_channels_data_map,
                                               data_container.rvrs_decomposed_channels_data_map)


def multimodal_image_df_to_result_image(data_container: DataContainer,
                                        output_name: str, output_width: int, output_height: int,
                                        output_format: OutputImageFormatEnum,
                                        visualization_channels_type: VisualizationChannelsEnum,
                                        channel_name_1: str = None, channel_name_2: str = None,
                                        channel_name_3: str = None):
    """
         multimodal_image_df_to_result_image creates an image from multimodal image df and saves it to file

         It can create an RGB, HSV or GrayScale image depending on visualization_channels_type value
    """

    VisualizationApi.df_to_image_and_save(data_container.get_image_df(),
                                          output_name, output_width, output_height, output_format,
                                          visualization_channels_type,
                                          data_container.standarized_channels_data_map,
                                          data_container.decomposed_channels_data_map,
                                          data_container.rvrs_decomposed_channels_data_map,
                                          data_container.converted_channels_data_map,
                                          channel_name_1, channel_name_2, channel_name_3)


def decomposed_image_channels_df_to_result_image(data_container: DataContainer,
                                                 output_name: str, output_width: int, output_height: int,
                                                 output_format: OutputImageFormatEnum,
                                                 visualization_channels_type: VisualizationChannelsEnum,
                                                 component_numbers_as_channels: [int]):
    """
         decomposed_image_channels_df_to_image_save_file creates an image from decomposed
            image (whole image decomposition)

         1.It can create an RGB, HSV or GrayScale image depending on visualization_channels_type value
         2.Whole image decomposition creates a df without channel names that would make sense, because the columns
            relate to decomposition components. For this reason they are named according to their indexes and this is
            how they should be passed to visualization method. e.g. component_numbers_as_channels = [1,2,3]
    """

    VisualizationApi.decomposed_image_channels_df_to_image_save_file(data_container.decomposed_image_data,
                                                                     output_name, output_width, output_height,
                                                                     output_format,
                                                                     visualization_channels_type,
                                                                     component_numbers_as_channels)


def decomposed_rvrs_dcmpsd_image_channels_df_to_result_image(data_container: DataContainer,
                                                             output_name: str, output_width: int, output_height: int,
                                                             output_format: OutputImageFormatEnum,
                                                             visualization_channels_type: VisualizationChannelsEnum,
                                                             component_numbers_as_channels: [int]):
    """
           decomposed_rvrs_dcmpsd_image_channels_df_to_result_image creates an image from reverse decomposed
            image (whole image reverse decomposition)

           1.It can create an RGB, HSV or GrayScale image depending on visualization_channels_type value
           2.Whole image reverse decomposition creates a df without channel names that would make sense, because the
            columns relate to decomposition components. For this reason they are named according to their indexes
             and this is how they should be passed to visualization method. e.g. component_numbers_as_channels = [1,2,3]
      """

    VisualizationApi.decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file(
        data_container.decomposed_rvrs_dcmpsd_image_df,
        output_name, output_width, output_height,
        output_format,
        visualization_channels_type,
        component_numbers_as_channels)


def decompose_single_channel(data_container: DataContainer, channel_name: str,
                             decomposition_type: DecompositionEnum, take_standarized_channel: bool,
                             fast_ica_n_components=None) -> (pd.DataFrame, [DecomposedChannelData]):
    """
           decompose_single_channel transforms a chosen channel using chosen decomposition type - PCA, FastICA, NMF

           1. Setting a take_standarized_channel flag to True will tell the library to decompose the standarized channel
           2. When choosing a FastICA mode it is necessary to manually provide a fast_ica_n_components value.


            The difference between this method and decompose_whole_image_channels is that it transforms one channel.
                It performs a decomposition only within it - as a result a channel with compressed width is received.
    """

    data_container.multimodal_image.image_df, data_container.decomposed_channels_data_map = \
        DecompositionApi.decompose_single_channel(data_container.get_image_df(),
                                                  data_container.get_channels_data_map(),
                                                  data_container.decomposed_channels_data_map,
                                                  data_container.standarized_channels_data_map,
                                                  channel_name,
                                                  decomposition_type, take_standarized_channel,
                                                  fast_ica_n_components)


def reverse_decompose_single_channel(data_container: DataContainer, channel_name: str):
    """
             reverse_decompose_single_channel performs a reverse decomposition on chosen channel according to the
             settings of an initial decomposition
    """

    data_container.multimodal_image.image_df, data_container.rvrs_decomposed_channels_data_map = \
        DecompositionApi.reverse_decompose_single_channel(data_container.get_image_df(), channel_name,
                                                          data_container.decomposed_channels_data_map,
                                                          data_container.rvrs_decomposed_channels_data_map)


def decompose_whole_image_channels(data_container: DataContainer, decomposition_type: DecompositionEnum,
                                   channel_names_and_take_std_tuple: [(str, bool)],
                                   fast_ica_n_components=None):
    """
           decompose_whole_image_channels transforms chosen multimodal image channels using chosen
            decomposition type - PCA, FastICA, NMF.

            The difference between this method and decompose_single_channel is that it transforms a whole image
            consisting of chosen channels. As a result image consisting of fewer channels is returned. It has the
            same resolution as input channels.

            1. Setting a take_std flag in channel_names_and_take_std_tuple to True for a specific channel
                will tell the library to take the standarized channel for decomposition
            2. When choosing a FastICA mode it is necessary to manually provide a fast_ica_n_components value.
    """

    data_container.decomposed_image_data = \
        DecompositionApi.decompose_whole_image_channels(data_container.get_image_df(), decomposition_type,
                                                        channel_names_and_take_std_tuple,
                                                        data_container.standarized_channels_data_map,
                                                        fast_ica_n_components)


def rvrs_decompose_whole_image_channels(data_container: DataContainer):
    """
         rvrs_decompose_whole_image_channels performs a reverse decomposition on whole image that was created with
         a decompose_whole_image_channels operation. It is done according to the settings of an initial decomposition
    """

    data_container.decomposed_rvrs_dcmpsd_image_df = DecompositionApi.rvrs_decompose_whole_image_channels(
        data_container.decomposed_image_data)


def convert_channel(data_container: DataContainer, channel_name: str, conversion_type: ConversionTypeEnum):
    """
        convert_channel performs a chosen conversion on a chosen channel.

        Possible conversions (conversion_type set to):
            1. INTENSITY - creates an intensity channel with pixel values in [0,255] range -
                                should be visualized in RGB mode
            2. DOLP - creates an DoLP image with pixel values in [0,1] range - should be visualized in HSV mode
            3. AOLP = 3 creates 9 new channels:
                - 3 of those are AoLP_HSV channels.
                - 3 of those are AoLP_Light_HSV channels. DoLP is set as AoLP saturation. Image is lighter and only the
                    polarized area is colored
                - 3 of those are AoLP_Dark_HSV channels. DoLP is set as AoLP value. Image is darker and only the
                    polarized area is colored
                Although all of them are already transformed to RGB values,
                    so they can be displayed in a regular, RGB mode.
    """

    data_container.multimodal_image.image_df, data_container.converted_channels_data_map = \
        ConversionApi.convert_channel(data_container.get_image_df(), data_container.get_channels_data_map(),
                                      channel_name, conversion_type, data_container.converted_channels_data_map)

# -----------------------------------------------------------------------------
