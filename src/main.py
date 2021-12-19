from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.channel.dto.channelInput import ChannelInput
from src.library.libraryApi import *

if __name__ == '__main__':
    data_container = DataContainer()
    load_multimodal_image_from_input(data_container, [
        ChannelInput(
            'resources/sample_images/ball/ball_0.png', [
                ChannelData('r', 8), ChannelData('g', 8), ChannelData('b', 8)
            ]
        ),
        ChannelInput(
            'resources/sample_images/ball/ball_45.png', [
                ChannelData('r1', 8), ChannelData('g1', 8), ChannelData('b1', 8)
            ]
        ),
    ])

    standarize_image_channels(data_container, ['g1'], {'r1': StandarizationModeEnum.BIT_SIZE_MIN_MAX})
    decompose_image_wrapper(data_container, DecompositionEnum.PCA)
    standarized_multimodal_image_df_to_image_save_file(data_container, 'test_hsv', 1024, 1024,
                                                       OutputImageFormatEnum.PNG, VisualizationChannelsEnum.GRAY_SCALE,
                                                       'r', 'g', 'b')

    # app = UiApplication()
