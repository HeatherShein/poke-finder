""" Notebook to clean csv and try to find pokemons
"""

# %%
# imports
import pandas as pd

# %%
# Test
df = pd.read_csv("../database/pokemons_cleant.csv")
df

# %%
# Test
df[df['name'] == 'Tortipouss']

# %%
# Clean csv
df = pd.read_csv("../database/pokemons.csv")
clean_df = df.T.drop("info").rename(columns={0: 'id', 1:'place', 2: 'place-type', 3: 'probability', 4: 'level'})
clean_df.to_csv("../database/pokemons_cleant.csv")

