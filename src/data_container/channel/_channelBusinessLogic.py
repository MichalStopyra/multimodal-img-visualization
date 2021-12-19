from src.data_container.channel.dto.channelData import ChannelData


def _find_channel_by_name(channel_data_map: [ChannelData], name: str) -> ChannelData:
    map_element = list(filter(lambda cdm: cdm.name == name, channel_data_map))
    if not map_element or len(map_element) != 1:
        raise Exception("Channel: {}'s data not specified", name)

    return map_element[0]
