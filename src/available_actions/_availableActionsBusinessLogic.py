import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData


def _find_all_initial_multimodal_img_channels(channels_data_map: [ChannelData]) -> [str]:
    result = []
    for channel in channels_data_map:
        result.append(channel.name)

    return result


def _find_all_df_channels(df: pd.DataFrame) -> [str]:
    return df.columns


