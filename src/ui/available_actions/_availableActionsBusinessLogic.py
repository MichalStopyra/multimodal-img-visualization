import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.decomposed_image.decomposedImage import DecomposedImage
from src.library.conversion.dto.ConvertedChannelData import ConvertedChannelData
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.properties.properties import \
    DECOMPOSED_WHOLE_IMAGE_SHORT_NAME, RVRS_DECOMPOSED_WHOLE_IMAGE_SHORT_NAME
from src.library.standarization.dto.destandarizedChannelData import DestandarizedChannelData
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum
from src.logger.loggerSettings import logger
from src.ui.available_actions.enum.actionTypeEnum import ActionTypeEnum


def _find_all_initial_multimodal_img_channels(channels_data_map: [ChannelData]) -> [str]:
    result = []
    for channel in channels_data_map:
        result.append(channel.name)

    return result


def _find_converted_df_channels(standarized_channels_data_map: [StandarizedChannelData],
                                destandarized_channels_data_map: [DestandarizedChannelData],
                                decomposed_channels_data_map: [DecomposedChannelData],
                                rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData],
                                converted_channels_data_map: [ConvertedChannelData],
                                decomposed_image_data: DecomposedImage,
                                decomposed_rvrs_dcmpsd_image_df: pd.DataFrame
                                ) -> [str]:
    channels = []

    if standarized_channels_data_map:
        for channel in standarized_channels_data_map:
            channels.append(channel.standarized_channel_name)

    if destandarized_channels_data_map:
        for channel in destandarized_channels_data_map:
            channels.append(channel.destandarized_channel_name)

    if decomposed_channels_data_map:
        for channel in decomposed_channels_data_map:
            channels.append(channel.decomposed_channel_name)

    if rvrs_decomposed_channels_data_map:
        for channel in rvrs_decomposed_channels_data_map:
            channels.append(channel.rvrs_decomposed_channel_name)

    if converted_channels_data_map:
        for channel in converted_channels_data_map:
            channels.append(channel.converted_channel_name)

    if decomposed_image_data:
        channels.append(DECOMPOSED_WHOLE_IMAGE_SHORT_NAME)

    if decomposed_rvrs_dcmpsd_image_df is not None:
        channels.append(RVRS_DECOMPOSED_WHOLE_IMAGE_SHORT_NAME)

    return channels


def _find_channels_available_for_action(action_type: ActionTypeEnum,
                                        channels_data_map: [ChannelData],
                                        standarized_channels_data_map: [StandarizedChannelData],
                                        destandarized_channels_data_map: [DestandarizedChannelData],
                                        decomposed_channels_data_map: [DecomposedChannelData],
                                        rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData],
                                        multimodal_img_df: pd.DataFrame,
                                        decomposed_image_data: DecomposedImage,
                                        rvrs_decomposed_image_df: pd.DataFrame,
                                        visualization_channel_type: VisualizationChannelsEnum,
                                        ) -> [(str, bool)]:
    channels_available_for_action = []
    if action_type == ActionTypeEnum.STANDARIZE_CHANNELS:
        for channel in channels_data_map:
            if not (list(filter(lambda std_ch: std_ch.initial_channel_name == channel.name,
                                standarized_channels_data_map))):
                channels_available_for_action.append((channel.name, True))

    elif action_type == ActionTypeEnum.DECOMPOSE_SINGLE_CHANNEL_RESOLUTION:
        for channel in channels_data_map:
            if not (list(filter(lambda dcmpsd_ch: dcmpsd_ch.initial_channel_name == channel.name,
                                decomposed_channels_data_map))):

                if (list(filter(lambda std_ch: std_ch.initial_channel_name == channel.name,
                                standarized_channels_data_map))):
                    std_ch_available = True
                else:
                    std_ch_available = False

                channels_available_for_action.append((channel.name, std_ch_available))

    elif action_type == ActionTypeEnum.REVERSE_DECOMPOSE_SINGLE_CHANNEL_RESOLUTION:
        for channel in channels_data_map:
            if (list(filter(lambda dcmpsd_ch: dcmpsd_ch.initial_channel_name == channel.name,
                            decomposed_channels_data_map))) \
                    and not (list(filter(lambda rvrs_dcmpsd_ch: rvrs_dcmpsd_ch.initial_channel_name == channel.name,
                                         rvrs_decomposed_channels_data_map))):
                channels_available_for_action.append((channel.name, False))

    elif action_type == ActionTypeEnum.DESTANDARIZE_CHANNEL:
        for channel in channels_data_map:
            if (list(filter(lambda std_ch: std_ch.initial_channel_name == channel.name,
                            standarized_channels_data_map))) \
                    and not (list(filter(lambda d_std_ch: d_std_ch.initial_channel_name == channel.name,
                                         destandarized_channels_data_map))):

                # Additionally, check if channel after rvrs decomposition can be destandarized
                if (list(filter(lambda rvrs_dcmpsd_ch: rvrs_dcmpsd_ch.initial_channel_name == channel.name,
                                rvrs_decomposed_channels_data_map))):
                    after_rvrs_dcmpsd_available = True
                else:
                    after_rvrs_dcmpsd_available = False

                channels_available_for_action.append((channel.name, after_rvrs_dcmpsd_available))

    elif action_type == ActionTypeEnum.CONVERT_CHANNEL:
        for channel in channels_data_map:
            channels_available_for_action.append((channel.name, False))

    elif action_type == ActionTypeEnum.DECOMPOSE_WHOLE_IMAGE_CHANNELS:
        for channel in channels_data_map:
            if (list(filter(lambda std_ch: std_ch.initial_channel_name == channel.name,
                            standarized_channels_data_map))):
                std_ch_available = True
            else:
                std_ch_available = False

            channels_available_for_action.append((channel.name, std_ch_available))

    elif action_type == ActionTypeEnum.REVERSE_DECOMPOSE_WHOLE_IMAGE_CHANNELS:
        logger.debug("Chose reverse decompose whole image channels! proceeding with no action...")

    elif action_type == ActionTypeEnum.DISPLAY_IMAGE_REGULAR_ACTIONS:
        if visualization_channel_type in (VisualizationChannelsEnum.GRAY_SCALE, VisualizationChannelsEnum.RGB):
            return multimodal_img_df.columns
        else:
            for channel in decomposed_channels_data_map:
                if channel.from_standarized_channel:
                    channels_available_for_action.append(channel.decomposed_channel_name)

            for channel in rvrs_decomposed_channels_data_map:
                if channel.from_standarized_channel:
                    channels_available_for_action.append(channel.rvrs_decomposed_channel_name)

            for channel in standarized_channels_data_map:
                channels_available_for_action.append(channel.standarized_channel_name)

            if len(channels_available_for_action) == 0:
                channels_available_for_action.append('-')

    elif action_type == ActionTypeEnum.DISPLAY_IMAGE_AFTER_WHOLE_IMG_DECOMPOSITION:
        if not decomposed_image_data:
            logger.debug("ERROR - No decomposed_image_data")
            return ['-']

        if visualization_channel_type == VisualizationChannelsEnum.HSV and not decomposed_image_data.image_standarized:
            channels_available_for_action.append('-')
        else:
            channels_available_for_action = decomposed_image_data.decomposed_image_df.columns

    elif action_type == ActionTypeEnum.DISPLAY_IMAGE_AFTER_WHOLE_IMG_RVRS_DECOMPOSITION:
        if rvrs_decomposed_image_df is None:
            logger.debug("ERROR - No rvrs decomposed_image_data")
            return ['-']

        for column in rvrs_decomposed_image_df.columns:
            channels_available_for_action.append(str(column))

    return channels_available_for_action

