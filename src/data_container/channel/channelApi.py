from src.data_container.channel._channelBusinessLogic import _find_channel_by_name
from src.data_container.channel.dto.channelData import ChannelData


class ChannelApi:

    @staticmethod
    def find_channel_by_name(channel_data_map: [ChannelData], name: str) -> ChannelData:
        return _find_channel_by_name(channel_data_map, name)
