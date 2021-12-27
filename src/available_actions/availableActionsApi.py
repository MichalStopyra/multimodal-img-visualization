from src.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.data_container.channel.dto.channelData import ChannelData
from src.available_actions._availableActionsBusinessLogic import _find_all_initial_multimodal_img_channels, \
    _find_all_df_channels, _find_channels_available_for_action
from src.data_container.dataContainer import DataContainer


class AvailableActionsApi:

    @staticmethod
    def find_all_initial_multimodal_img_channels(data_container: DataContainer):
        data_container.initial_channel_names = _find_all_initial_multimodal_img_channels(
            data_container.get_channels_data_map())


    @staticmethod
    def find_all_df_channels(data_container: DataContainer):
        data_container.available_channel_names = _find_all_df_channels(
            data_container.get_image_df())

    @staticmethod
    def find_channels_available_for_action(data_container: DataContainer,
                                           action_type: ActionTypeEnum) -> [(str, bool)]:
        return _find_channels_available_for_action(action_type,
                                                   data_container.get_channels_data_map(),
                                                   data_container.standarized_channels_data_map,
                                                   data_container.destandarized_channels_data_map,
                                                   data_container.decomposed_channels_data_map,
                                                   data_container.rvrs_decomposed_channels_data_map)