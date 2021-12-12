class OutputFormatEnum:
    PNG = 1
    JPG = 2
    JPEG = 3


def translate_output_format_enum(output_format: OutputFormatEnum) -> str:
    if output_format == OutputFormatEnum.PNG:
        return '.png'
    elif output_format == OutputFormatEnum.JPG:
        return '.jpg'
    elif output_format == OutputFormatEnum.JPEG:
        return '.jpeg'
    else:
        raise Exception("ERROR: Disallowed output format!")
