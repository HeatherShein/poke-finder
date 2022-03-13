""" Script to find pokemon based on name or id (national or regional)
"""

# Imports
import argparse
import pandas as pd


# Converts string with level range to the max level we can find
def str_to_max_lvl(str_level: str):
    return int(str_level.split("-")[-1])


# Fuse several place dicts to one when they have the same place
def fuse_place_dict(array_place):
    i = 0
    while i < len(array_place) - 1:
        if array_place[i]["place"] == array_place[i + 1]["place"]:
            for key in array_place[i + 1].keys():
                array_place[i][key] = array_place[i + 1][key]
            array_place.pop(i + 1)
        else:
            i += 1
    return array_place


# Print required information
def print_places(places):
    for place in places:
        print(f"# Place: {place['place']}")
        print()
        for key in place.keys():
            if key != "place":
                print(f"# {key}: {place[key]}")
        print()


# Find pokemon definition
def find_pokemon(**kwargs):
    """Finds a pokemon based on specific criterions
    Parameters
    ----------
    name: str (name of the pokemon)
    id: int (id to filter it)

    Output
    ----------
    None
    """
    # Open database
    df = pd.read_csv(
        "./data/sinnoh/pokemons.csv"
    )  # TODO: change this according to region
    if kwargs["name"] is not None:
        criteria, criteria_type = kwargs["name"], "name"
    elif kwargs["id"] is not None:
        criteria, criteria_type = kwargs["id"], "id"
    else:
        print("Error: you should pass one argument between name and id")
        return

    # Find places
    row = df[df[criteria_type] == criteria]
    if len(row) > 0:  # This pokemon exists
        if criteria_type == "id":
            intro = f"Pokémon #{criteria} : {row.name.values[0]}"
        else:
            intro = f"Pokémon #{row.id.values[0]}: {criteria}"
        print(f"# ---------- # {intro} # ---------- #")
        print()
        print()
        places = row.places.values[0]
        if places != "[]":  # This pokemon is found on places
            # Clean places (pandas does not correctly support array in cells)
            places = places[1:-1].replace("'", "").replace(" ", "").split(",")
            prob = 0
            lvl = 0
            all_places = []
            max_prob_places = []
            max_lvl_places = []
            # Print informations for each route
            # TODO: change this with required information (max prob)
            for place in places:
                # TODO: change this according to region
                place_df = pd.read_csv("data/sinnoh/routes/" + place + ".csv")
                row = place_df[place_df[criteria_type] == criteria]
                values = {
                    x: row[x].values[0]
                    for x in [
                        "place_type",
                        "probability_M",
                        "probability_J",
                        "probability_N",
                        "probability_DE",
                        "probability_PS",
                        "level_M",
                        "level_J",
                        "level_N",
                    ]
                }

                values["place"] = place
                for key in values.keys():
                    if key.startswith("level"):
                        max_lvl = str_to_max_lvl(values[key])
                        if max_lvl > lvl:
                            max_lvl_places = [
                                {
                                    "place": place,
                                    "place_type": values["place_type"],
                                    key: values[key],
                                }
                            ]
                            lvl = max_lvl
                        elif max_lvl == lvl:
                            max_lvl_places.append(
                                {
                                    "place": place,
                                    "place_type": values["place_type"],
                                    key: values[key],
                                }
                            )
                    if key.startswith("probability"):
                        if values[key] > prob:
                            max_prob_places = [
                                {
                                    "place": place,
                                    "place_type": values["place_type"],
                                    key: values[key],
                                }
                            ]
                            prob = values[key]
                        # To print all places with the same max prob
                        elif values[key] == prob:
                            max_prob_places.append(
                                {
                                    "place": place,
                                    "place_type": values["place_type"],
                                    key: values[key],
                                }
                            )

                all_places.append(values)

            if kwargs["max_prob"]:
                print_places(fuse_place_dict(max_prob_places))
            elif kwargs["max_lvl"]:
                print_places(fuse_place_dict(max_lvl_places))
            else:
                print_places(all_places)
        else:
            print(df[df[criteria_type] == criteria].localisation)
    else:
        print(
            f"Error: {criteria} not found in database\
            (either mispelled or not in right region)."
        )


# Main definition
def main():
    """Console script to find pokemons"""
    # Create parser
    parser = argparse.ArgumentParser()

    # Configure arguments
    parser.add_argument("--name", type=str)
    parser.add_argument("--id", type=int)
    parser.add_argument(
        "--max-prob",
        action="store_true",
        help="shows only the place where we can find the pokemon at max probability",
    )
    parser.add_argument(
        "--max-lvl",
        action="store_true",
        help="shows only the place where we can find the pokemon at the highest level",
    )

    # Read arguments
    try:
        args = parser.parse_args()
        parsed_args_dict = {k: v for k, v in vars(args).items() if k != "func"}
        find_pokemon(**parsed_args_dict)
    except Exception as err:
        print(err)
        return 1
    return 0


if __name__ == "__main__":
    main()
