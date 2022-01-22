from src.data_container.channel.dto.channelData import ChannelData


def _find_channel_by_name_and_raise_exception(channel_data_map: [ChannelData], name: str) -> ChannelData:
    if not channel_data_map:
        return None

    map_element_list = list(filter(lambda cdm: cdm.name == name, channel_data_map))
    if not map_element_list or len(map_element_list) != 1:
        raise Exception("Channel: {}'s data not specified", name)

    return map_element_list[0]

def _channel_(channel_data_map: [ChannelData], name: str) -> ChannelData:
    if not channel_data_map:
        return None

    map_element_list = list(filter(lambda cdm: cdm.name == name, channel_data_map))
    if not map_element_list or len(map_element_list) != 1:
        raise Exception("Channel: {}'s data not specified", name)

    return map_element_list[0]


def _check_if_channel_name_occupied(channel_data_map: [ChannelData], name: str) -> bool:
    if not channel_data_map:
        return False

    map_element_list = list(filter(lambda cdm: cdm.name == name, channel_data_map))
    return map_element_list is not None and len(map_element_list) > 0
