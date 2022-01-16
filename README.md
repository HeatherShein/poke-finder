# Poke Finder

> Small tool to find which spot is the best to hunt a specific pokemon.
> Made by webscrapping pokebip.com.
> Only available for Sinnoh Region (Yet?)

* Auteur: Colin Davidson
* Date de création: 2022-01-12


## Table of contents

1. [General info](#general-info)
2. [Installing Project](#installing-project)
2. [Use the app](#use-the-app)
3. [Data](#data)
4. [Files and folders](#files-and-folders)
5. [How to contribute](#how-to-contribute)


## General info

### Description

This project is a small tool that helps knowing where to hunt a specific pokemon with the highest probability.
All the data used in the project was scrapped from [Pokébip](https://pokebip.com).

### Technology

This project was developed using :

* Python 3.6.9
* Pandas 1.1.5
* BeautifulSoup 4.10.0

### Example

```sh
python3 finder.py --name="Pikachu"

# ---------- # Pokémon #25: Pikachu # ---------- #


# Place: manoir-pokemon

# place_type: Hautes herbes
# probability_M: 10
# probability_J: 10
# probability_N: 10
# probability_DE: 10
# probability_PS: 10
# level: 18


python3 finder.py --id=200

# ---------- # Pokémon #200 : Feuforêve # ---------- #


# Place: foret-vestigion

# place_type: Hautes herbes
# probability_M: 20
# probability_J: 20
# probability_N: 20
# probability_DE: 20
# probability_PS: 20
# level: 10-11

# Place: tour-perdue

# place_type: Au sol
# probability_M: 20
# probability_J: 20
# probability_N: 20
# probability_DE: 20
# probability_PS: 20
# level: 17
```

## Installing project

After cloning the project, you may need to install some packages. To do so, follow these commands :

```sh
# Create virtual environment (feel free to use whatever you want)
virtualenv venv
source venv/bin/activate
# Install packages
pip install pandas beautifulsoup4 requests
```

Then, to install the database :

```sh
# Move to the data folder (from project's root)
cd data
# Launch creation
python3 create_database.py
```


## Use the app

The app is command-line based. To look for a pokemon, you may use :

```sh
# On project's root
# To find by name
python3 finder.py --name="Your Pokemon's Name"
# To find by id
python3 finder.py --id=your_id
```


## Data

Data was previously scrapped on pokebip.com.

To understand what is going on, check [This file](./docs/data.md)


## Files and Folders

```bash
.
├── data                    # database folder, in which data is scrapped and stored
│   ├── sinnoh              # region folder
│   |    ├── routes         # routes folder
│   |    ├── places.txt     # text file indicating with webpage to scrap
│   |    ├── stopwords.txt  # text file indicating which table name to ignore
│   |    ├── pokemons.csv   # csv file containing infos on pokemons once scrapped
│── docs                    # folder containing additionnal documentation
├── notebooks               # folder with notebooks to make some tests
├── finder.py               # main file to execute
├── README.md               # this file
```

## How to contribute

To contribute you are invited to read those [guidelines](./docs/contribution.md)