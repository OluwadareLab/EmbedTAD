import time
import numpy as np
import cugraph as cg
import pandas as pd
import dask.dataframe as dd
 
print("Reading dataset into Pandas DataFrame as an edgelist...")
st = time.time()
x = np.loadtxt("/home/mohit/Documents/project/EmbedTAD/data/matrix/GM12878_insitu_primary_30_10000_chr21.mat")
x_df = pd.DataFrame(x)
src, dest = np.where(x_df.to_numpy() != 0)
weights = x_df.values[src, dest]
edges_df = pd.DataFrame({
    's': src,
    'd': dest,
    'w': weights
})
print(f"{edges_df.head(2)}")
print("Creating Graph from Pandas DataFrame edgelist...")
st = time.time()
G = cg.from_pandas_edgelist(
    edges_df, source="s", destination="d", edge_attr="w", create_using=cg.Graph(directed=False)
)
print(f"done, time: {(time.time() - st):.6f}s")