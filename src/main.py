from src.input_data.channel.channelInput import ChannelInput
from src.input_data.channel.channelNameAndBitSize import ChannelNameAndBitSize
from src.input_data.inputData import InputData
from src.ui.uiApplication import UiApplication

if __name__ == '__main__':
    a = InputData([
        ChannelInput(
            'resources/sample_images/ball/ball_0.png', [
                ChannelNameAndBitSize('r', 8), ChannelNameAndBitSize('g', 8), ChannelNameAndBitSize('b', 8)
            ]
        ),
        ChannelInput(
            'resources/sample_images/ball/ball_0.png', [
                ChannelNameAndBitSize('r1', 8), ChannelNameAndBitSize('g1', 8), ChannelNameAndBitSize('b1', 8)
            ]
        ),
    ])
    # app = UiApplication()
