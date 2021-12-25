import pandas as pd


class DecomposedImage:
    def __init__(self, decomposed_image_df: pd.DataFrame, image_standarized: bool, decomposition_object: any):
        self.decomposed_image_df = decomposed_image_df
        self.image_standarized = image_standarized
        self.decomposition_object = decomposition_object
