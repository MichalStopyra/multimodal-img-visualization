import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.library.conversion.dto.ConvertedChannelData import ConvertedChannelData
from src.library.conversion.enum.conversionTypeEnum import ConversionTypeEnum
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum


def _validate_channel_indexes(component_numbers_as_channels: [int], image_df: pd.DataFrame):
    if image_df.shape[1] < max(component_numbers_as_channels):
        raise Exception("ERROR - highest channel index bigger than the amount of channels of decomposed image")


def _validate_number_of_channels_for_decomposed_image_channels(visualization_channels_type: VisualizationChannelsEnum,
                                                               channels_nr: int):
    if visualization_channels_type == VisualizationChannelsEnum.GRAY_SCALE:
        if channels_nr > 1:
            print("WARNING - gray scale image can only have 1 channel, while: ", channels_nr, " has been chosen!\n",
                  "Taking the first one")
    else:
        if channels_nr > 3:
            print("WARNING - ", visualization_channels_type, " image can only have 3 channel, while: ", channels_nr,
                  " has been chosen!\n", "Taking the first three")
        if channels_nr < 3:
            raise Exception("ERROR - ", visualization_channels_type, " image requires 3 channels!")


def _validate_gray_scale_channels(channel_name_1, channel_name_2, channel_name_3,
                                  decomposed_channels_data_map: [DecomposedChannelData],
                                  rvrs_decomposed_channels_data_map,
                                  std_channels_data_map):
    if not channel_name_1:
        raise Exception("ERROR: In order to produce gray scale image, channel_1 needs to be specified!")
    if channel_name_2 or channel_name_3:
        print("WARNING: Gray scale image chosen - channels 2 and 3 will be omitted")
    if __is_given_channel_of_standarized_type(channel_name_1, std_channels_data_map, decomposed_channels_data_map,
                                              rvrs_decomposed_channels_data_map):
        print("WARNING: Gray scale image chosen - provided standarized channel! Output will not make any sense!")


def __validate_rgb_channels(channel_name_1, channel_name_2, channel_name_3,
                            decomposed_channels_data_map: [DecomposedChannelData], rvrs_decomposed_channels_data_map,
                            std_channels_data_map, converted_channels_data_map):
    if not channel_name_1 or not channel_name_2 or not channel_name_3:
        raise Exception('ERROR - In order to create hsv image - pass 3 channel names!')

    for channel_name in [channel_name_1, channel_name_2, channel_name_3]:
        if __is_given_channel_of_standarized_type(channel_name, std_channels_data_map, decomposed_channels_data_map,
                                                  rvrs_decomposed_channels_data_map, converted_channels_data_map):
            print("WARNING: RGB image chosen - channel ", channel_name, " is standarized!")


def __raise_exception_if_channels_not_standarized(channel_names_list: [ChannelData],
                                                  std_channels_data_map: [StandarizedChannelData],
                                                  decomposed_channel_data_map: [DecomposedChannelData],
                                                  rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData],
                                                  converted_channels_data_map: [ConvertedChannelData]):
    for channel_name in channel_names_list:
        if not __is_given_channel_of_standarized_type(channel_name, std_channels_data_map, decomposed_channel_data_map,
                                                      rvrs_decomposed_channels_data_map, converted_channels_data_map):
            raise Exception("Error: HSV image requires standarized channels data! channel: ",
                            channel_name, " not standarized!")


def _raise_exception_if_empty_df_or_wrong_channel_names(df: pd.DataFrame,
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
                                           decomposed_channels_data_map: [DecomposedChannelData],
                                           rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData],
                                           converted_channels_data_map: [ConvertedChannelData],
                                           ) -> bool:
    std_map_element_list = list(filter(
        lambda channel: channel.standarized_channel_name == channel_name, std_channels_data_map))

    decomposed_map_standarized_element_list = list(filter(
        lambda channel: channel.decomposed_channel_name == channel_name and channel.from_standarized_channel,
        decomposed_channels_data_map))

    rvrs_decomposed_map_standarized_element_list = list(filter(
        lambda channel: channel.rvrs_decomposed_channel_name == channel_name and channel.from_standarized_channel,
        rvrs_decomposed_channels_data_map))

    converted_map_standarized_element_list = list(filter(
        lambda channel: channel.converted_channel_name == channel_name
                        and channel.conversion_type == ConversionTypeEnum.DOLP, converted_channels_data_map))

    return (std_map_element_list is not None and len(std_map_element_list) != 0) \
           or (decomposed_map_standarized_element_list is not None
               and len(decomposed_map_standarized_element_list) != 0) \
           or (rvrs_decomposed_map_standarized_element_list is not None
               and len(rvrs_decomposed_map_standarized_element_list) != 0) \
           or (converted_map_standarized_element_list is not None
               and len(converted_map_standarized_element_list) != 0)


def _validate_if_channels_standarized(visualization_channels_type: VisualizationChannelsEnum,
                                      image_standarized: bool):
    if visualization_channels_type == VisualizationChannelsEnum.HSV:
        if not image_standarized:
            raise Exception("Error: HSV image requires standarized channels data!")
    else:
        if image_standarized:
            print("WARNING - Provided standarized image channels for RGB / GrayScale Image!")
