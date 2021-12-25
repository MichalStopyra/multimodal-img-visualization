from src.data_container.channel.dto.channelData import ChannelData
from src.data_container.channel.dto.channelInput import ChannelInput
from src.library.libraryApi import *
from src.library.properties.properties import *

if __name__ == '__main__':
    data_container = DataContainer()
    load_multimodal_image_from_input(data_container, [
        ChannelInput(
            'resources/sample_images/ball/ball_hsv_B.png', [
                ChannelData('r', 8), ChannelData('g', 8), ChannelData('b', 8)
            ]
        ),

        ChannelInput(
            'resources/sample_images/ball/ball_AoLP.png', [
                ChannelData('a', 8), ChannelData('L', 8), ChannelData('P', 8)
            ]
        ),
    ])

    standarize_image_channels(data_container, [], {
        'r': StandarizationModeEnum.BIT_SIZE_MIN_MAX,
        'g': StandarizationModeEnum.BIT_SIZE_MIN_MAX,
        'b': StandarizationModeEnum.BIT_SIZE_MIN_MAX
    })

    decompose_channel_resolution_wrapper(data_container, 'r', DecompositionEnum.PCA, True)
    decompose_channel_resolution_wrapper(data_container, 'g', DecompositionEnum.FAST_ICA, True, 2)
    decompose_channel_resolution_wrapper(data_container, 'b', DecompositionEnum.PCA, True)

    reverse_decompose_channel(data_container, 'r')
    reverse_decompose_channel(data_container, 'g')
    reverse_decompose_channel(data_container, 'b')

    destandarize_channel_by_name(data_container, 'r', True)
    destandarize_channel_by_name(data_container, 'g', True)
    destandarize_channel_by_name(data_container, 'b', True)

    decompose_image_channels_wrapper(data_container, DecompositionEnum.PCA,
                                     [('r', True), ('g', True), ('b', True), ('a', True), ('L', True), ('P', True)])

    rvrs_decompose_image_channels(data_container)

    decomposed_image_channels_df_to_image_save_file(data_container, 'test_dcmpsd', 1024, 1024,
                                                    OutputImageFormatEnum.PNG, VisualizationChannelsEnum.GRAY_SCALE,
                                                    [1, 2, 3])

    # TODO dodac destandaryzacje razy 255 i drukowanie po indeksach
    # Dodatkowo listowanie dostepnych kanalow??

    multimodal_image_df_to_image_save_file(data_container, 'test', 1024, 1024,
                                           OutputImageFormatEnum.PNG, VisualizationChannelsEnum.HSV,
                                           DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'r',
                                           DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'g',
                                           DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'b')

    # app = UiApplication()
