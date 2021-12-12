from src.input_data.channel.channelInput import ChannelInput
from src.input_data.channel.channelData import ChannelData
from src.input_data.inputData import InputData
from src.ui.uiApplication import UiApplication

if __name__ == '__main__':
    a = InputData([
        ChannelInput(
            'resources/sample_images/ball/ball_0.png', [
                ChannelData('r', 8), ChannelData('g', 8), ChannelData('b', 8)
            ]
        ),
        ChannelInput(
            'resources/sample_images/ball/ball_0.png', [
                ChannelData('r1', 8), ChannelData('g1', 8), ChannelData('b1', 8)
            ]
        ),
    ])
    # app = UiApplication()
