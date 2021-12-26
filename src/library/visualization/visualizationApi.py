import numpy as np
import pandas as pd

from src.data_container.decomposed_image.decomposedImage import DecomposedImage
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData
from src.library.visualization._decomposedImageVisualizationBusinessLogic import \
    _decomposed_image_channels_df_to_image_save_file, _decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file
from src.library.visualization._visualizationBusinessLogic import _save_img, _df_to_image_and_save
from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum


class VisualizationApi:

    @staticmethod
    def df_to_image_and_save(df: pd.DataFrame, output_name: str,
                             output_width: int, output_height: int, output_format: OutputImageFormatEnum,
                             visualization_channels_type: VisualizationChannelsEnum,
                             std_channels_data_map: [StandarizedChannelData],
                             decomposed_channels_data_map: [DecomposedChannelData],
                             rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData],
                             channel_name_1: str = None, channel_name_2: str = None, channel_name_3: str = None):
        _df_to_image_and_save(df, output_name, output_width, output_height,
                              output_format,
                              visualization_channels_type,
                              std_channels_data_map, decomposed_channels_data_map, rvrs_decomposed_channels_data_map,
                              channel_name_1, channel_name_2, channel_name_3)

    @staticmethod
    def save_img(image_array: np.ndarray, image_name: str, image_format: OutputImageFormatEnum):
        _save_img(image_array, image_name, image_format)

    @staticmethod
    def decomposed_image_channels_df_to_image_save_file(decomposed_image_data: DecomposedImage,
                                                        output_name: str,
                                                        output_width: int, output_height: int,
                                                        output_format: OutputImageFormatEnum,
                                                        visualization_channels_type: VisualizationChannelsEnum,
                                                        component_numbers_as_channels: [int]):
        _decomposed_image_channels_df_to_image_save_file(decomposed_image_data,
                                                         output_name, output_width, output_height,
                                                         output_format, visualization_channels_type,
                                                         component_numbers_as_channels)

    @staticmethod
    def decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file(decomposed_rvrs_dcmpsd_image_df: pd.DataFrame,
                                                                    output_name: str,
                                                                    output_width: int, output_height: int,
                                                                    output_format: OutputImageFormatEnum,
                                                                    visualization_channels_type: VisualizationChannelsEnum,
                                                                    component_numbers_as_channels: [int]):
        _decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file(decomposed_rvrs_dcmpsd_image_df,
                                                                     output_name, output_width, output_height,
                                                                     output_format, visualization_channels_type,
                                                                     component_numbers_as_channels)
