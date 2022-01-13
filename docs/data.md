# Data

## I. Data structure on website

On [Pokébip](https://pokebip.com), data about pokemons is organized by place (routes, canal...). Therefore, there is one URL per place.

In each webpage, there are tables containing informations about pokemons you can find in every type of place (water, on the ground...) but also other unrequired information (enemies, objects...). These information are thus filtered to only keep pokemons.

*Note : some pages contain information about special pokemons (legendaries or not), these pokemons don't have the info we need, so we disregard them too.*

## II. Data structure on poke finder

When scraping every place of the region, informations about pokemon are only kept for the place with the highest probability to drop this pokemon (example : Etourmi has 50% chance to appear on route-201 and 40% chance on route-202, thus route-201 is kept).

Once this filtering is done, data is organized by pokemon rather than by place.

