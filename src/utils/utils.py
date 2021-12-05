import numpy as np
import pandas as pd


def array_to_df(input_array: np.array) -> pd.DataFrame:
    new_shape = input_array.reshape(-1, input_array.shape[2])
    df = pd.DataFrame(data=new_shape)
    df.columns = [f'channel{i}' for i in range(1, 1 + new_shape.shape[1])]
    return df
