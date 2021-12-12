from src.input_data.channel.channelData import ChannelData


class ReadyChannel:
    def __init__(self, image, channels_names_and_bit_sizes: [ChannelData]):
        self.image = image
        self.channels_names_and_bit_sizes = channels_names_and_bit_sizes
