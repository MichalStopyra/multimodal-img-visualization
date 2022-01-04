from src.data_container.dataContainer import DataContainer
from src.ui.dialog.channelInputDialog import UiChannelInputDialog
from src.ui.dialog.uiChooseChannelOneStdDialog import UiChooseChannelOneStdDialog


def open_channel_input_dialog(main_window, data_container: DataContainer):
    main_window.channel_input_dialog = UiChannelInputDialog(data_container)
    main_window.channel_input_dialog.show()


def open_choose_channel_one_std_dialog(main_window, data_container: DataContainer):
    main_window.choose_channel_one_std_dialog = UiChooseChannelOneStdDialog(data_container)
    main_window.choose_channel_one_std_dialog.show()
