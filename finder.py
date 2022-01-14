""" Script to find pokemon based on name or id (national or regional)
"""

# Imports
import argparse
import pandas as pd


def find_by_name(df, name):
    """Finds infos about a pokemon based on a name
    Parameters
    ----------
    df: DataFrame
    name: str (name of the pokemon)

    Output
    ----------
    None
    """
    # Find places
    row = df[df["name"] == name]
    if len(row) > 0:  # This pokemon exists
        print(f"# ---------- # {name} # ---------- #")
        print()
        print()
        places = row.places
        if len(places) > 0:  # This pokemon is found on places
            # Clean places (pandas does not correctly support array in cells)
            places = places.values[0][1:-1].replace("'", "").replace(" ", "").split(",")

            # Print informations for each route
            # TODO: change this with required information (max prob)
            for place in places:
                # TODO: change this according to region
                place_df = pd.read_csv("../data/sinnoh/routes/" + place + ".csv")
                row = place_df[place_df["name"] == name]
                values = {
                    x: row[x].values[0] for x in ["place_type", "probability", "level"]
                }
                print(f"# Place: {place}")
                print()
                print(
                    f"# Place_type: {values['place_type']},\
                    Probability: {values['probability']}, Level: {values['level']}"
                )
        else:
            print(df[df["name"] == name].localisation)
    else:
        print(
            f"Error: {name} not found in database (either mispelled or not in right region)."
        )


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
        places = row.places
        if len(places) > 0:  # This pokemon is found on places
            # Clean places (pandas does not correctly support array in cells)
            places = places.values[0][1:-1].replace("'", "").replace(" ", "").split(",")

            # Print informations for each route
            # TODO: change this with required information (max prob)
            for place in places:
                # TODO: change this according to region
                place_df = pd.read_csv("data/sinnoh/routes/" + place + ".csv")
                row = place_df[place_df[criteria_type] == criteria]
                values = {
                    x: row[x].values[0] for x in ["place_type", "probability", "level"]
                }
                print(f"# Place: {place}")
                print(
                    f"# Place_type: {values['place_type']},\
                    Probability: {values['probability']}, Level: {values['level']}"
                )
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
