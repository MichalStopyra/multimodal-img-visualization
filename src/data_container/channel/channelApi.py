from src.data_container.channel._channelBusinessLogic import _find_channel_by_name, _check_if_channel_name_occupied
from src.data_container.channel.dto.channelData import ChannelData


class ChannelApi:

    @staticmethod
    def find_channel_by_name(channel_data_map: [ChannelData], name: str) -> ChannelData:
        return _find_channel_by_name(channel_data_map, name)

    @staticmethod
    def check_if_channel_name_occupied(channel_data_map: [ChannelData], name: str) -> bool:
        return _check_if_channel_name_occupied(channel_data_map, name)
