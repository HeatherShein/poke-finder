""" Script to find pokemon based on name or id (national or regional)
"""

# Imports
import argparse
import pandas as pd


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
                print(f"# Place: {place}")
                print()
                for key in values.keys():
                    print(f"# {key}: {values[key]}")
                print()
        else:
            print(df[df[criteria_type] == criteria].localisation)
    else:
        print(
            f"Error: {criteria} not found in database\
            (either mispelled or not in right region)."
        )


# Main definition
def main():
    """ Console script to find pokemons """
    # Create parser
    parser = argparse.ArgumentParser()

    # Configure arguments
    parser.add_argument("--name", type=str)
    parser.add_argument("--id", type=int)

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
