""" Script to create a database of routes with pokemons on it (id, name, probability of spawning, level)
"""

# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup


# scrap webpage definition
def scrap_page(url):
    """ Scraps a web page to extract informations based on specific tables
    Parameters
    ----------
    url: str (webpage to scrap)

    Output
    ----------
    route_dict: dict (informations on pokemons about one page)
    """
    # Get webpage
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get tables
    tables = soup.find_all('table')

    # Create dictionnary
    route_dict = {}

    # Read stopwords
    with open('stopwords.txt') as file:
        stopwords = file.readlines()
    for i, stopword in enumerate(stopwords):
        stopword = stopword.replace('\n', '')
        stopwords[i] = stopword
    
    # Fill informations about pokemons
    for table in tables:
        if table.tr.th.text not in stopwords: # Get rid of other types of table
            trs = table.find_all('tr')
            if len(trs) > 2: # At least one pokemon to scrap
                place_type = trs[0].th.text # First row contains type of place to find pokemons
                route_dict[place_type] = {}
                for i in range(2, len(trs)): # For each pokemon
                    tds = trs[i].find_all('td')
                    if len(tds) > 5:
                        id, name, prob, level = tds[0].text, tds[2].text, tds[4].text, tds[5].text
                        route_dict[place_type][id] = {'name': name, 'probability': prob, 'level': level}

    # Return infos
    return route_dict


# Main definition
def main():
    # Define routes to scrap
    main_url = 'https://www.pokebip.com/page/jeuxvideo/pokemon-diamant-etincelant-perle-scintillante/guide-des-lieux/'
    with open("places.txt") as file:
        urls = file.readlines()

    # Define final dictionnary
    all_routes_dict = {}

    # Scrap each url
    for url in urls:
        url = url.replace('\n', '')
        print(url)
        all_routes_dict[url] = scrap_page(main_url + url)

    # Convert route dict into pokemon dict
    pokemon_dict = {}
    for route_name, route_dict in all_routes_dict.items():
        for place_type, pokemon in route_dict.items():
            for id, value in pokemon.items():
                exist = value['name'] in pokemon_dict
                better_chances = exist and pokemon_dict[value['name']]['probability'] < value['probability']
                if not exist or better_chances:
                    # Create new / Update row
                    pokemon_dict[value['name']] = {'id': id, 'place': route_name, 'place_type': place_type, 'probability': value['probability'], 'level': value['level']}

    # Save as csv
    pokemon_df = pd.DataFrame(pokemon_dict)
    pokemon_df.to_csv("pokemons.csv")



if __name__ == '__main__':
    main()