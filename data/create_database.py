""" Script to create a database of routes with pokemons on it
(id, name, probability of spawning, level)
"""

# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup


# Scrap pokemons definition
def scrap_pokemons():
    """Scraps every pokemon info based on national pokedex
    Parameters
    ----------
    None

    Output
    ----------
    pokemon_df: DataFrame
    """
    # Get web page
    main_url = "https://www.pokebip.com/page/jeuxvideo/"
    region_url = "pokemon-diamant-etincelant-perle-scintillante/pokedex-national"
    r = requests.get(main_url + region_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get table (only one table to consider)
    table = soup.table

    # Declare pokemon dictionnary
    pokemon_dict = {"id": [], "name": [], "localisation": [], "places": []}

    # Get every information on pokemon
    trs = table.find_all("tr")
    for i in range(1, len(trs)):
        tds = trs[i].find_all("td")
        pokemon_dict["id"].append(tds[0].text)
        pokemon_dict["name"].append(tds[2].text)
        pokemon_dict["localisation"].append(tds[3].text)
        pokemon_dict["places"].append([])

    # Convert to dataframe
    pokemon_df = pd.DataFrame.from_dict(pokemon_dict)

    # Return infos
    return pokemon_df


# scrap webpage definition
def scrap_page(url, region):
    """Scraps a web page to extract informations based on specific tables
    Parameters
    ----------
    url: str (webpage to scrap)
    region: str (region of pokemon)

    Output
    ----------
    route_df: DataFrame (informations on pokemons about one page)
    """
    # Get webpage
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get tables
    tables = soup.find_all("table")

    # Create dictionnary
    route_dict = {
        "id": [],
        "name": [],
        "place_type": [],
        "probability": [],
        "level": [],
    }

    # Read stopwords
    with open(region + "/stopwords.txt") as file:
        stopwords = file.readlines()
    for i, stopword in enumerate(stopwords):
        stopword = stopword.replace("\n", "")
        stopwords[i] = stopword

    # Fill informations about pokemons
    for table in tables:
        if table.tr.th.text not in stopwords:  # Get rid of other types of table
            trs = table.find_all("tr")
            if len(trs) > 2:  # At least one pokemon to scrap
                place_type = trs[
                    0
                ].th.text  # First row contains type of place to find pokemons
                for i in range(2, len(trs)):  # For each pokemon
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

    # Convert to DataFrame
    route_df = pd.DataFrame.from_dict(route_dict)

    # Return infos
    return route_df


# Main definition
def main():
    region = "sinnoh"
    # Get pokemon_df
    print("Creating pokemon table")
    pokemon_df = scrap_pokemons()

    # Define routes to scrap
    # TODO: change depending on region
    main_url = "https://www.pokebip.com/page/jeuxvideo/"
    region_url = "pokemon-diamant-etincelant-perle-scintillante/guide-des-lieux/"

    with open(region + "/places.txt") as file:
        urls = file.readlines()

    # Define final dictionnary
    all_routes_dict = {}

    # Scrap each url
    print("Start scrapping...")
    for url in urls:
        url = url.replace("\n", "")
        print(url)
        all_routes_dict[url] = scrap_page(main_url + region_url + url, region)

    print("Start enriching pokemon table")
    # Enrich pokemon_df with place presence
    for route_name, route_df in all_routes_dict.items():
        # Enrich pokemon_df with place
        def update_place(row):
            if route_df["id"].isin([row["id"]]).any():
                row["places"].append(route_name)
            return row

        pokemon_df = pokemon_df.apply(update_place, axis=1)
        # Save route dataframe
        route_df.to_csv(region + "/routes/" + route_name + ".csv")

    # Save as csv
    pokemon_df.to_csv(region + "/pokemons.csv")


if __name__ == "__main__":
    main()
