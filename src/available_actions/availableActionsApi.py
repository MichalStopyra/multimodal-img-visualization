from src.data_container.channel.dto.channelData import ChannelData
from src.available_actions._availableActionsBusinessLogic import _find_all_initial_multimodal_img_channels, \
    _find_all_df_channels
from src.data_container.dataContainer import DataContainer


class AvailableActionsApi:

    @staticmethod
    def find_all_initial_multimodal_img_channels(data_container: DataContainer) -> [str]:
        data_container.initial_channel_names = _find_all_initial_multimodal_img_channels(
            data_container.get_channels_data_map())


    @staticmethod
    def find_all_df_channels(data_container: DataContainer) -> [str]:
        data_container.available_channel_names = _find_all_df_channels(
            data_container.get_image_df())


