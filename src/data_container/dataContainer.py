import pandas as pd

from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.channel.dto.channelInput import ChannelInputInterface
from src.data_container.multimodal_image.multimodalImage import MultimodalImage


class DataContainer:
    def __init__(self):
        self.multimodal_image = None  # type MultimodalImage

        # Single channel decomposition (decreasing channel resolution)
        self.decomposed_channels_data_map = []
        self.rvrs_decomposed_channels_data_map = []

        self.standarized_channels_data_map = []
        self.destandarized_channels_data_map = []

        # Whole image decomposition (decreasing the amount of channels)
        self.decomposed_image_data = None  # type DecomposedImage
        self.decomposed_rvrs_dcmpsd_image_df = None

    def get_channels_data_map(self) -> [ChannelData]:
        if self.multimodal_image:
            return self.multimodal_image.channels_data_map
        else:
            return None

    def get_image_df(self) -> pd.DataFrame:
        return self.multimodal_image.image_df

    def load_multimodal_image_from_input(self, channels_inputs: [ChannelInputInterface]):
        self.multimodal_image = MultimodalImage(channels_inputs)

    def add_channels_to_multimodal_img(self, channels_inputs: [ChannelInputInterface]):
        if self.multimodal_image:
            self.multimodal_image.add_channels_to_multimodal_img(channels_inputs)
        else:
            self.load_multimodal_image_from_input(channels_inputs)

    def print_image_df_head(self):
        print(self.get_image_df().head())
