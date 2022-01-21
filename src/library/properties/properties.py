from typing import Final

from src.library.visualization.enum.outputImageFormatEnum import OutputImageFormatEnum

PCA_VARIATION_MIN_VALUE: Final = 0.99

OUTPUT_IMAGE_PATH: Final = 'resources/output_images/'
OUTPUT_IMAGE_NAME_RESULT: Final = 'result'
OUTPUT_IMAGE_FORMAT: Final = OutputImageFormatEnum.PNG
OUTPUT_IMAGE_WIDTH: Final = 1024
OUTPUT_IMAGE_HEIGHT: Final = 1024
STD_MAX_PIXEL_VALUE: Final = 255

STANDARIZED_CHANNEL_NAME_TEMPLATE: Final = 'std_'
DESTANDARIZED_CHANNEL_NAME_TEMPLATE: Final = 'd-std_'

DESTANDARIZED_AFTER_DECOMPOSITION_CHANNEL_NAME_TEMPLATE: Final = 'd-std_dcmpsd_'

DECOMPOSED_CHANNEL_NAME_TEMPLATE: Final = 'dcmpsd_'
REVERSE_DECOMPOSED_CHANNEL_NAME_TEMPLATE: Final = 'rvrs_dcmpsd_'

DECOMPOSED_WHOLE_IMAGE_NAME_TEMPLATE: Final = 'decomposed_image_channels'

CONVERTED_CHANNEL_INTENSITY_NAME_TEMPLATE: Final = 'intensity_'
CONVERTED_CHANNEL_DOLP_NAME_TEMPLATE: Final = 'DoLP_'
CONVERTED_CHANNEL_AOLP_NAME_TEMPLATE: Final = 'AoLP_'


DECOMPOSED_WHOLE_IMAGE_SHORT_NAME: Final = 'decomposed_image'
RVRS_DECOMPOSED_WHOLE_IMAGE_SHORT_NAME: Final = 'rvrs_decomposed_image'
