import os
import random

import pandas as pd

# Load the data
df = pd.read_json("data.json")
files = os.listdir("poster_downloads")


def change_image(x):
    x["image"] = os.path.join("poster_downloads", random.choice(files))
    return x


df["fields"] = df["fields"].apply(change_image)

df.to_json("data_new.json", orient="records")
