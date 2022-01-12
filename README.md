# Poke Finder

> Small tool to find which spot is the best to hunt a specific pokemon
> Made by webscrapping pokebip.com
> Only available for Sinnoh Region (Diamond / Pearl)

* Auteur: Colin Davidson
* Date de création: 2022-01-12


## Table of contents

1. [Installing Project](#installing-project)
2. [Use the app](#use-the-app)
3. [Data](#data)
4. [Folders](#folders)


## Installing project

After cloning the project, you may need to install some packages. To do so, follow these commands :

```
# Create virtual environment (feel free to use whatever you want)
virtualenv venv
source venv/bin/activate
# Install packages
pip install pandas beautifulsoup4 requests
```


## Use the app

The app is command-line based. To look for a pokemon, you may use :

```
# On project's root
# To find by name
python3 finder.py --name="Your Pokemon's Name"
# To find by id (National or Regional id is indicated with the second argument)
python3 finder.py --id=your_id --national=True/False
```


## Data

Data was previously scrapped on pokebip.com.

To understand what is going on, check database/create_database.py


## Folders

```bash
.
├── database            # database folder, in which data is scrapped and stored
├── notebooks           # folder with notebooks to make some tests
```