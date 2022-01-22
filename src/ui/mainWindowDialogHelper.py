from src.data_container.dataContainer import DataContainer
from src.ui.dialog.chooseChannelsStandarization import UiChooseChannelsStandarization
from src.ui.dialog.uiChannelInputDialog import UiChannelInputDialog
from src.ui.dialog.uiChooseChannelConversion import uiChooseChannelConversion
from src.ui.dialog.uiChooseChannelDecomposeSingleChannel import UiChooseChannelDecomposeSingleChannel
from src.ui.dialog.uiChooseChannelDestandarization import UiChooseChannelDestandarization
from src.ui.dialog.uiChooseChannelRvrsDecomposition import UiChooseChannelRvrsDecomposition
from src.ui.dialog.uiChooseChannelsDecomposeWholeImg import UiChooseChannelsDecomposeWholeImg
from src.ui.dialog.uiChooseChannelsDisplayImg import UiChooseChannelsDisplayImg
from src.ui.dialog.uiChooseChannelsDisplayImgWholeImgDecomposition import \
    UiChooseChannelsDisplayImgWholeImgDecomposition


def open_channel_input_dialog(main_window, data_container: DataContainer):
    main_window.channel_input_dialog = UiChannelInputDialog(data_container)
    main_window.channel_input_dialog.show()


def open_choose_channel_destandarization(main_window, data_container: DataContainer):
    main_window.choose_channel_destandarization = UiChooseChannelDestandarization(data_container)
    main_window.choose_channel_destandarization.show()


def open_choose_channel_decompose_single_channel(main_window, data_container: DataContainer):
    main_window.choose_channel_decompose_single_channel = UiChooseChannelDecomposeSingleChannel(data_container)
    main_window.choose_channel_decompose_single_channel.show()


def open_choose_channel_rvrs_decomposition(main_window, data_container: DataContainer):
    main_window.choose_channel_rvrs_decomposition = UiChooseChannelRvrsDecomposition(data_container)
    main_window.choose_channel_rvrs_decomposition.show()


def open_choose_channels_decompose_whole_img(main_window, data_container: DataContainer):
    main_window.choose_channels_decompose_whole_img = UiChooseChannelsDecomposeWholeImg(data_container)
    main_window.choose_channels_decompose_whole_img.show()


def open_choose_channels_display_img(main_window, data_container: DataContainer):
    main_window.choose_channels_display_img = UiChooseChannelsDisplayImg(data_container)
    main_window.choose_channels_display_img.show()


def open_choose_channels_display_img_whole_img_decomposition(main_window, data_container: DataContainer):
    main_window.choose_channels_display_img_whole_img_decomposition = \
        UiChooseChannelsDisplayImgWholeImgDecomposition(data_container)
    main_window.choose_channels_display_img_whole_img_decomposition.show()


def open_choose_channels_standarization(main_window, data_container: DataContainer):
    main_window.choose_channels_standarization = UiChooseChannelsStandarization(data_container)
    main_window.choose_channels_standarization.show()


def open_choose_channels_conversion(main_window, data_container: DataContainer):
    main_window.choose_channels_conversion = uiChooseChannelConversion(data_container)
    main_window.choose_channels_conversion.show()
