import pandas as pd

BASE_PATH = "/home/mohit/Documents/project/EmbedTAD/data/resutls/comparison"
ORGANISM = ["gm12878", "ch12lx"]
RESOLUTIONS = ["5K", "10K"]
ALGORITHMS = ["Caspian", "EmbedTAD", "IC_Finder"]

df = pd.read_csv(f"{BASE_PATH}/gm12878/5K/EmbedTAD_1.bed",
                 delimiter="\t", header=None)
df = df.iloc[:, [1, 3]]
df.to_csv(f"{BASE_PATH}/gm12878/5K/EmbedTAD.bed",
          sep=",", header=None, index=False)
