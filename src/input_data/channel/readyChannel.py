from src.input_data.channel.channelNameAndBitSize import ChannelNameAndBitSize


class ReadyChannel:
    def __init__(self, image, channels_names_and_bit_sizes: [ChannelNameAndBitSize]):
        self.image = image
        self.channels_names_and_bit_sizes = channels_names_and_bit_sizes
