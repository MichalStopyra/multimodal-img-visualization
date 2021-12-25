import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.channel.dto.channelInput import ChannelInputInterface
from src.data_container.multimodal_image.multimodalImage import MultimodalImage


class DataContainer:
    def __init__(self):
        self.multimodal_image = None # type MultimodalImage

        self.decomposed_channels_data_map = []
        self.rvrs_decomposed_channels_data_map = []

        self.standarized_channels_data_map = []
        self.destandarized_channels_data_map = []

        self.decomposed_image_data = None # type DecomposedImage
        self.rvrs_decomposed_image_df = None

    def get_channels_data_map(self) -> [ChannelData]:
        return self.multimodal_image.channels_data_map

    def get_image_df(self) -> pd.DataFrame:
        return self.multimodal_image.image_df

    def load_multimodal_image_from_input(self, channels_inputs: [ChannelInputInterface]):
        self.multimodal_image = MultimodalImage(channels_inputs)

    def print_image_df_head(self):
        print(self.get_image_df().head())
