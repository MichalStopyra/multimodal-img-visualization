class OutputImageFormatEnum:
    PNG = 1
    JPG = 2
    JPEG = 3


def translate_output_format_enum(output_format: OutputImageFormatEnum) -> str:
    if output_format == OutputImageFormatEnum.PNG:
        return '.png'
    elif output_format == OutputImageFormatEnum.JPG:
        return '.jpg'
    elif output_format == OutputImageFormatEnum.JPEG:
        return '.jpeg'
    else:
        raise Exception("ERROR: Disallowed output format!")
