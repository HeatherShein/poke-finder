""" Notebook to clean csv and try to find pokemons
"""

# %%
# imports
import pandas as pd

# %%
# read csv
df = pd.read_csv("../data/sinnoh/pokemons.csv")
df

# %%
# find places
places = df[df["name"] == "Nosferapti"].places.values[0]
# clean places
places = places[1:-1].replace("'", "").replace(" ", "").split(",")
places

# %%
# Compare each route
for place in places:
    place_df = pd.read_csv("../data/sinnoh/routes/" + place + ".csv")
    row = place_df[place_df["name"] == "Nosferapti"]
    print(
        f"Place: {place}, Place_type: {row['place_type'].values[0]},\
        Probability: {row['probability'].values[0]}, Level: {row['level'].values[0]}"
    )

# %%
# find places
places = df[df["id_national"] == 41].places.values[0]
# clean places
places = places[1:-1].replace("'", "").replace(" ", "").split(",")
places

# %%
# Test
for place in places:
    place_df = pd.read_csv("../data/sinnoh/routes/" + place + ".csv")
    row = place_df[place_df["id"] == 41]
    print(
        f"Place: {place}, Place_type: {row['place_type'].values[0]},\
        Probability: {row['probability'].values[0]}, Level: {row['level'].values[0]}"
    )

# %%
# Clean csv
df = pd.read_csv("../database/pokemons.csv")
clean_df = df.T.drop("info").rename(
    columns={0: "id", 1: "place", 2: "place-type", 3: "probability", 4: "level"}
)
clean_df.to_csv("../database/pokemons_cleant.csv")
