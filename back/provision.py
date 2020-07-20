from pokedex.managers import pokemons, types

types.load_types_from_api()
pokemons.load_all_pokemons_from_api()
