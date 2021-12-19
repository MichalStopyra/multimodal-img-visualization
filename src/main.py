from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.channel.dto.channelInput import ChannelInput
from src.library.libraryApi import *
from src.library.properties.properties import REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE

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

    standarize_image_channels(data_container, ['g1'], {
        'r': StandarizationModeEnum.BIT_SIZE_MIN_MAX,
        'g': StandarizationModeEnum.BIT_SIZE_MIN_MAX,
        'b': StandarizationModeEnum.BIT_SIZE_MIN_MAX
    })
    decompose_channel_wrapper(data_container, 'r', DecompositionEnum.PCA)
    decompose_channel_wrapper(data_container, 'g', DecompositionEnum.PCA)
    decompose_channel_wrapper(data_container, 'b', DecompositionEnum.PCA)

    reverse_decompose_channel(data_container, 'r')
    reverse_decompose_channel(data_container, 'g')
    reverse_decompose_channel(data_container, 'b')

    multimodal_image_df_to_image_save_file(data_container, 'test_hsv', 1024, 1024,
                                           OutputImageFormatEnum.PNG, VisualizationChannelsEnum.RGB,
                                           REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'r',
                                           REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'g',
                                           REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'b')

    # app = UiApplication()
