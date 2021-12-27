import pandas as pd

from src.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.decomposed_image.decomposedImage import DecomposedImage
from src.library.decomposition.dto.decomposedChannelData import DecomposedChannelData
from src.library.decomposition.dto.reverseDecomposedChannelData import ReverseDecomposedChannelData
from src.library.properties.properties import DECOMPOSED_WHOLE_IMAGE_NAME_TEMPLATE
from src.library.standarization.dto.destandarizedChannelData import DestandarizedChannelData
from src.library.standarization.dto.standarizedChannelData import StandarizedChannelData
from src.logger.loggerSettings import logger


def _find_all_initial_multimodal_img_channels(channels_data_map: [ChannelData]) -> [str]:
    result = []
    for channel in channels_data_map:
        result.append(channel.name)

    return result


def _find_all_df_channels(df: pd.DataFrame) -> [str]:
    return df.columns


def _find_channels_available_for_action(action_type: ActionTypeEnum,
                                        channels_data_map: [ChannelData],
                                        standarized_channels_data_map: [StandarizedChannelData],
                                        destandarized_channels_data_map: [DestandarizedChannelData],
                                        decomposed_channels_data_map: [DecomposedChannelData],
                                        rvrs_decomposed_channels_data_map: [ReverseDecomposedChannelData]
                                        ) -> [(str, bool)]:
    channels_available_for_action = []
    if action_type == ActionTypeEnum.STANDARIZE_CHANNELS:
        for channel in channels_data_map:
            if not (list(filter(lambda std_ch: std_ch.initial_channel_name == channel.name,
                                standarized_channels_data_map))):
                channels_available_for_action.append((channel.name, False))

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
            if not (list(filter(lambda d_std_ch: d_std_ch.initial_channel_name == channel.name,
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

    elif action_type == ActionTypeEnum.DISPLAY_IMAGE:
        logger.debug("Chose displaying image! proceeding with no action...")

    return channels_available_for_action

#
# def _displaying_image_options(decomposed_image_data :DecomposedImage,
#                               whole_rvrs_decomposed_image_exists: bool):
#     options_available = []
#     if decomposed_image_data:
#
#         options_available.append((DECOMPOSED_WHOLE_IMAGE_NAME_TEMPLATE,
#                                               whole_rvrs_decomposed_image_exists))
