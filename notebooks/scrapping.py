""" Notebook to test scrapping pokemons from pokebip.com
"""
# %%
# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup

# %%
# Get webpage
url = "https://www.pokebip.com/page/jeuxvideo/pokemon-diamant-etincelant-perle-scintillante/guide-des-lieux/grand-marais"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# %%
# Get tables
tables = soup.find_all('table')
len(tables)

# %%
# Create dictionnary
route_dict = {}

# %%
# Inspect tables
for table in tables:
    if table.tr.th.text not in ['Dresseur', 'Img.', ' ', 'Spiritomb', ' Bloupi ♀']:
        trs = table.find_all('tr')
        if len(trs) > 2: # At least one pokemon to scrap
            place_type = trs[0].th.text
            route_dict[place_type] = {}
            for i in range(2, len(trs)):
                tds = trs[i].find_all('td')
                if len(tds) > 5:
                    id, name, prob, level = tds[0].text, tds[2].text, tds[4].text, tds[5].text
                    route_dict[place_type][id] = {'name': name, 'probability': prob, 'level': level}

route_dict

# %%
# Test
tables[3].tr.th.text


# %%
# Test
pokemon_dict = {}
for key, pokemon in route_dict.items():
    for id, value in pokemon.items():
        if value['name'] not in pokemon_dict:
            pokemon_dict[value['name']] = {'place_type': key, 'probability': value['probability'], 'level': value['level']}
        else:
            if pokemon_dict[value['name']]['probability'] < value['probability']:
                # Replace all
                pass

pokemon_dict

# %%
# Test
pokemon_dict = {'Étourmi': {'id': '396', 'place': 'route-201', 'place_type': 'Hautes herbes', 'probability': '50%M./J.40%Nuit', 'level': '2-3'}, 'Keunotor-': {'id': '399', 'place': 'route-201', 'place_type': 'Hautes herbes', 'probability': '50%M./J.60%Nuit', 'level': '2-3'}, 'Nidoran♀-': {'id': '29', 'place': 'route-201', 'place_type': 'Poké Radar', 'probability': '20%DE2%PS', 'level': '3DE2PS'}, 'Nidoran♂-': {'id': '32', 'place': 'route-201', 'place_type': 'Poké Radar', 'probability': '2%DE20%PS', 'level': '2DE3PS'}, 'Doduo': {'id': '84', 'place': 'route-201', 'place_type': 'Troupeaux', 'probability': '40%', 'level': '2'}, 'Crikzik-': {'id': '401', 'place': 'route-202', 'place_type': 'Hautes herbes', 'probability': '10%Mat.20%Nuit', 'level': '3Matin3-4Nuit'}, 'Lixy-': {'id': '403', 'place': 'route-202', 'place_type': 'Hautes herbes', 'probability': '30%', 'level': '3-4'}, 'Fouinette-': {'id': '161', 'place': 'route-202', 'place_type': 'Poké Radar', 'probability': '22%', 'level': '2-4'}, 'Zigzaton-': {'id': '263', 'place': 'route-202', 'place_type': 'Troupeaux', 'probability': '40%', 'level': '3'}}
pd.DataFrame(pokemon_dict)