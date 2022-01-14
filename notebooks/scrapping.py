""" Notebook to test scrapping pokemons from pokebip.com
"""
# %%
# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup

# %%
# Get webpage
main_url = "https://www.pokebip.com/page/jeuxvideo/"
region_url = "pokemon-diamant-etincelant-perle-scintillante/pokedex-national"
r = requests.get(main_url + region_url)
soup = BeautifulSoup(r.content, "html.parser")

# %%
# Get tables
tables = soup.find_all("table")
len(tables)

# %%
# Test
soup.table

# %%
# Declare pokemon dictionnary
pokemon_dict = {"id_national": [], "name": [], "localisation": [], "places": []}

# %%
# Test
trs = tables[0].find_all("tr")

# %%
# Test
trs[1]

# %%
# Get every information on pokemon
for i in range(1, len(trs)):
    tds = trs[i].find_all("td")
    pokemon_dict["id_national"].append(tds[0].text)
    pokemon_dict["name"].append(tds[2].text)
    pokemon_dict["localisation"].append(tds[3].text)
    pokemon_dict["places"].append([])

pokemon_dict

# %%
# Convert to dataframe
df = pd.DataFrame.from_dict(pokemon_dict)
df

# %%
# Test
df[df.index == 1]["places"]

# %%
# Get webpage
main_url = "https://www.pokebip.com/page/jeuxvideo/"
region_url = (
    "pokemon-diamant-etincelant-perle-scintillante/guide-des-lieux/mont-couronne"
)
r = requests.get(main_url + region_url)
soup = BeautifulSoup(r.content, "html.parser")

# %%
# Get tables
tables = soup.find_all("table")
len(tables)

# %%
# Create dictionnary
route_dict = {"id": [], "name": [], "place_type": [], "probability": [], "level": []}

# %%
# Inspect tables
for table in tables:
    if table.tr.th.text not in ["Dresseur", "Img.", " ", "Spiritomb", " Bloupi ♀"]:
        trs = table.find_all("tr")
        if len(trs) > 2:  # At least one pokemon to scrap
            place_type = trs[0].th.text
            for i in range(2, len(trs)):
                tds = trs[i].find_all("td")
                if len(tds) > 5:
                    id, name, prob, level = (
                        tds[0].text,
                        tds[2].text,
                        tds[4].text,
                        tds[5].text,
                    )
                    route_dict["id"].append(id)
                    route_dict["name"].append(name)
                    route_dict["place_type"].append(place_type)
                    route_dict["probability"].append(prob)
                    route_dict["level"].append(level)

route_dict

# %%
# Convert to df
route_df = pd.DataFrame.from_dict(route_dict)
route_df


# %%
# Test
def update_place(row):
    if route_df["id"].isin([row["id_national"]]).any():
        row["places"].append("route-201")
    return row


test_df = df.apply(update_place, axis=1)

# %%
# Test
for index, row in test_df.iterrows():
    if row["places"] != []:
        print(row)
print("Fini")

# %%
# Test
df[df["name"] == "Korillon"]

# %%
# Test
tables[3].tr.th.text


# %%
# Test
pokemon_dict = {}
for key, pokemon in route_dict.items():
    for id, value in pokemon.items():
        if value["name"] not in pokemon_dict:
            pokemon_dict[value["name"]] = {
                "place_type": key,
                "probability": value["probability"],
                "level": value["level"],
            }
        else:
            if pokemon_dict[value["name"]]["probability"] < value["probability"]:
                # Replace all
                pass

pokemon_dict
