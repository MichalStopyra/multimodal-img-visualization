import scipy.io as sio

from src.utils.utils import *


def load_and_convert_mat_to_df(image_path):
    input_dict = sio.loadmat(image_path)
    # [3][1]??
    input_list = list(input_dict.items())[3][1]
    input_array = np.array(input_list)
    return array_to_df(input_array)


class FileReader:
    # class used for reading and normalizing the multimodal data -
    def __init__(self, image_path):
        self.input_df = load_and_convert_mat_to_df(image_path)
