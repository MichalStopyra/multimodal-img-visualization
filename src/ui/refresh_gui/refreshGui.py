from PyQt5 import QtWidgets, Qt

from src.data_container.dataContainer import DataContainer
from src.ui.available_actions.availableActionsApi import AvailableActionsApi


def refresh_gui(appWindow):
    __set_channels_lists(appWindow.data_container, appWindow.list_widget_multimodal_image_channels,
                         appWindow.listWidget_converted_channels)
    __calculate_buttons_enabled(appWindow.data_container, appWindow.toolButton_standarize_channels,
                                appWindow.toolButton_decompose_single_channel_resolution,
                                appWindow.toolButton_reverse_decompose_single_channel_resolution,
                                appWindow.toolButton_destandarize_channel_by_name,
                                appWindow.toolButton_convert_channel,
                                appWindow.toolButton_decompose_whole_image,
                                appWindow.toolButton_rvrs_decompose_whole_image,
                                appWindow.toolButton_display_img,
                                appWindow.toolButton_reset,
                                appWindow.toolButton_display_img_2)


def __set_channels_lists(data_container: DataContainer,
                         init_channels_list: QtWidgets.QListWidget, converted_channels_list: QtWidgets.QListWidget
                         ) -> (QtWidgets.QListWidget, QtWidgets.QListWidget):
    if data_container.multimodal_image:
        init_channels = AvailableActionsApi.find_all_initial_multimodal_img_channels(data_container)
        if init_channels:
            for channel in init_channels:
                if not init_channels_list.findItems(channel, Qt.Qt.MatchExactly):
                    init_channels_list.addItem(channel)

        converted_channels = AvailableActionsApi.find_converted_df_channels(data_container)
        if converted_channels:
            for channel in converted_channels:
                if not converted_channels_list.findItems(channel, Qt.Qt.MatchExactly):
                    converted_channels_list.addItem(channel)

    return init_channels_list, converted_channels_list


def __calculate_buttons_enabled(data_container: DataContainer,
                                toolButton_standarize_channels: QtWidgets.QToolButton,
                                toolButton_decompose_single_channel_resolution: QtWidgets.QToolButton,
                                toolButton_reverse_decompose_single_channel_resolution: QtWidgets.QToolButton,
                                toolButton_destandarize_channel_by_name: QtWidgets.QToolButton,
                                toolButton_convert_channel: QtWidgets.QToolButton,
                                toolButton_decompose_whole_image: QtWidgets.QToolButton,
                                toolButton_rvrs_decompose_whole_image: QtWidgets.QToolButton,
                                toolButton_display_img: QtWidgets.QToolButton,
                                toolButton_reset: QtWidgets.QToolButton,
                                toolButton_display_img_2: QtWidgets.QToolButton
                                ):
    toolButton_standarize_channels.setEnabled(data_container.multimodal_image is not None)
    toolButton_decompose_single_channel_resolution.setEnabled(data_container.multimodal_image is not None)
    toolButton_reverse_decompose_single_channel_resolution.setEnabled(
        data_container.decomposed_channels_data_map is not None
        and len(data_container.decomposed_channels_data_map) > 0)
    toolButton_destandarize_channel_by_name.setEnabled(data_container.standarized_channels_data_map is not None
                                                       and len(data_container.standarized_channels_data_map) > 0)
    toolButton_convert_channel.setEnabled(data_container.multimodal_image is not None)
    toolButton_decompose_whole_image.setEnabled(data_container.multimodal_image is not None)
    toolButton_rvrs_decompose_whole_image.setEnabled(data_container.decomposed_image_data is not None)
    toolButton_display_img.setEnabled(data_container.multimodal_image is not None)
    toolButton_display_img_2.setEnabled(data_container.decomposed_image_data is not None)
    converted_df_channels = AvailableActionsApi.find_converted_df_channels(data_container)
    toolButton_reset.setEnabled(converted_df_channels is not None and len(converted_df_channels) > 0)
