from src.available_actions.availableActionsApi import AvailableActionsApi
from src.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.data_container.channel.dto.channelInput import ChannelInput
from src.library.libraryApi import *
from src.ui.uiApplication import UiApplication

if __name__ == '__main__':
    data_container = DataContainer()
    # app = UiApplication()

    load_new_multimodal_image_from_input(data_container, [
        ChannelInput(
            'resources/sample_images/ball/ball_hsv_B.png',
            [
                ('r', 8), ('g', 8), ('b', 8)
            ]
        ),

        ChannelInput(
            'resources/sample_images/ball/ball_AoLP.png',
            [
                ('a', 8), ('L', 8), ('P', 8)
            ]
        ),
    ])

    add_channels_to_multimodal_img(data_container, [
        ChannelInput(
            'resources/sample_images/ball/ball_hsv_B.png',
            [
                ('t', 8), ('t2', 8), ('t1', 8)
            ]
        ),

        ChannelInput(
            'resources/sample_images/ball/ball_AoLP.png',
            [
                ('s', 8), ('s1', 8), ('s2', 8)
            ]
        ),
    ])
    AvailableActionsApi.find_channels_available_for_action(data_container, ActionTypeEnum.STANDARIZE_CHANNELS)
    standarize_image_channels(data_container, ["P"], {
        'r': StandarizationModeEnum.BIT_SIZE_MIN_MAX,
        'g': StandarizationModeEnum.BIT_SIZE_MIN_MAX,
        'b': StandarizationModeEnum.BIT_SIZE_MIN_MAX
    })

    # decompose_channel_resolution_wrapper(data_container, 'r', DecompositionEnum.PCA, True)
    # decompose_channel_resolution_wrapper(data_container, 'r', DecompositionEnum.NMF, True)
    # decompose_channel_resolution_wrapper(data_container, 'g', DecompositionEnum.FAST_ICA, True, 2)
    # decompose_channel_resolution_wrapper(data_container, 'b', DecompositionEnum.PCA, True)
    #
    # reverse_decompose_channel(data_container, 'r')
    # reverse_decompose_channel(data_container, 'g')
    # reverse_decompose_channel(data_container, 'b')
    #
    # destandarize_channel_by_name(data_container, 'r', True)
    # destandarize_channel_by_name(data_container, 'g', True)
    # destandarize_channel_by_name(data_container, 'b', True)
    #
    # decompose_image_channels_wrapper(data_container, DecompositionEnum.PCA,
    #                                  [('r', True), ('g', True), ('b', True), ('a', True), ('L', True), ('P', False)])
    #

    # rvrs_decompose_image_channels(data_container)
    #
    # decomposed_image_channels_df_to_image_save_file(data_container, 'test_dcmpsd', 1024, 1024,
    #                                                 OutputImageFormatEnum.PNG, VisualizationChannelsEnum.HSV,
    #                                                 [1, 2, 3])
    #
    # decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file(data_container, 'test_rvrs_dcmpsd', 1024, 1024,
    #                                                             OutputImageFormatEnum.PNG,
    #                                                             VisualizationChannelsEnum.RGB,
    #                                                             [1, 2, 3])
    #
    # AvailableActionsApi.find_all_initial_multimodal_img_channels(data_container)
    # AvailableActionsApi.find_all_df_channels(data_container)
    #
    # multimodal_image_df_to_image_save_file(data_container, 'test', 1024, 1024,
    #                                        OutputImageFormatEnum.PNG, VisualizationChannelsEnum.HSV,
    #                                        DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'r',
    #                                        DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'g',
    #                                        DECOMPOSED_CHANNEL_NAME_TEMPLATE + 'b')

