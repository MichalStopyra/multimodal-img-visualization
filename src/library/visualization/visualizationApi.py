import numpy as np
import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.library.visualization._visualizationBusinessLogic import _save_img, _df_to_image_and_save
from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum


class VisualizationApi:

    @staticmethod
    def df_to_image_and_save(df: pd.DataFrame, channel_data_map: [ChannelData], destandarize: bool, output_name: str,
                             output_width: int, output_height: int, output_format: OutputImageFormatEnum,
                             output_channels_type: VisualizationChannelsEnum,
                             channel_name_1: str = None, channel_name_2: str = None, channel_name_3: str = None):
        _df_to_image_and_save(df, channel_data_map, destandarize, output_name, output_width, output_height,
                              output_format,
                              output_channels_type,
                              channel_name_1, channel_name_2, channel_name_3)

    @staticmethod
    def save_img(image_array: np.ndarray, image_name: str, image_format: OutputImageFormatEnum):
        _save_img(image_array, image_name, image_format)

    # @staticmethod
    # def decomposed_df_to_image_and_save(df: pd.DataFrame, channel_data_map: [ChannelData], destandarize: bool,
    #                                     output_name: str,
    #                                     output_width: int, output_height: int, output_format: OutputImageFormatEnum,
    #                                     output_channels_type: VisualizationChannelsEnum):
    #     _decomposed_df_to_image_and_save(df, channel_data_map, destandarize, output_name, output_width, output_height,
    #                                      output_format,
    #                                      output_channels_type)
