""" Script to find pokemon based on name or id (national or regional)
"""

# Imports
import argparse
import pandas as pd


# Find pokemon definition
def find_pokemon(**kwargs):
    """ Finds a pokemon based on specific criterions
    Parameters
    ----------
    name: str (name of the pokemon)
    id: int (id to filter it)
    national: bool (boolean whether to look for national index or not)

    Output
    ----------
    None
    """
    # Open database
    df = pd.read_csv("./database/pokemons_cleant.csv")
    if kwargs['name'] is not None:
        name = kwargs['name']
        if len(df[df['name'] == name]) != 0:
            print(df[df['name'] == name])
        else:
            print("Error, name not found (either mispelled or not in database)")
    if kwargs['id'] is not None:
        id = kwargs['id']
        if kwargs['national'] is True:
            new_id = id
        else:
            new_id = id + 386 # Offset to regional pokedex
        if len(df[df['id'] == new_id]) != 0:
                print(df[df['id'] == new_id])
        else:
            print("Error, id not found (not in database)")


# Main definition
def main():
    """ Console script to find pokemons """
    # Create parser
    parser = argparse.ArgumentParser()

    # Configure arguments
    parser.add_argument('--name', type=str)
    parser.add_argument('--id', type=int)
    parser.add_argument('--national', type=bool, default=False)

    # Read arguments
    try:
        args = parser.parse_args()
        parsed_args_dict = {k: v for k, v in vars(args).items() if k != 'func'}
        find_pokemon(**parsed_args_dict)
    except Exception as err:
        print(err)
        return 1
    return 0


if __name__ == "__main__":
    main()