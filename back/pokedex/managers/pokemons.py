import requests
from playhouse.shortcuts import update_model_from_dict

from pokedex.errors.not_found import PokemonNotFoundError
from pokedex.models.pokemon import (
    Pokemon,
    Type,
    PokemonTypes,
)


def get_pokemon_by_name(name):
    pokemon = Pokemon.get_or_none(name=name)
    if pokemon is None:
        raise PokemonNotFoundError(name)

    return pokemon


def create_pokemon(name, hp, special_attack, defense, attack, special_defense, speed):
    stats = {
        "hp": hp,
        "special_attack": special_attack,
        "defense": defense,
        "attack": attack,
        "special_defense": special_defense,
        "speed": speed,
    }
    try:
        pokemon = get_pokemon_by_name(name)
        update_model_from_dict(pokemon, stats)
        pokemon.save()
    except PokemonNotFoundError:
        pokemon = Pokemon.create(name=name, **stats)

    return pokemon


def load_pokemon_from_api(name):
    request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    pokemon_data = request.json()

    stats = {}
    for stat in pokemon_data["stats"]:
        stat_name = stat["stat"]["name"].replace("-", "_")
        stat_value = int(stat["base_stat"])

        stats[stat_name] = stat_value

    sprite_front = pokemon_data["sprites"]["front_default"]
    sprite_back = pokemon_data["sprites"]["back_default"]

    pokemon = Pokemon.get_or_none(name=name)
    data = {"sprite_front": sprite_front, "sprite_back": sprite_back, **stats}
    if pokemon is None:
        pokemon = Pokemon.create(name=name, **data)
    else:
        update_model_from_dict(pokemon, data)
        pokemon.save()

    return pokemon


def load_pokemon_types_from_api(name):
    request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    pokemon_data = request.json()

    pokemon = get_pokemon_by_name(name)
    PokemonTypes.delete().where(PokemonTypes.pokemon == pokemon).execute()

    types = []
    for api_type in pokemon_data["types"]:
        type_name = api_type["type"]["name"]

        type = Type.get_or_none(name=type_name)
        pokemon_type = PokemonTypes.create(
            pokemon=pokemon, type=type, slot=api_type["slot"]
        )

        types.append(pokemon_type)

    return types


def load_all_pokemons_from_api():
    i = 0

    next_page = "https://pokeapi.co/api/v2/pokemon/"
    while next_page is not None:
        request = requests.get(next_page)
        pokemons_data = request.json()

        # next_page = pokemons_data["next"]
        next_page = None

        for pokemon in pokemons_data["results"]:
            load_pokemon_from_api(pokemon["name"])
            load_pokemon_types_from_api(pokemon["name"])
            i += 1

        print(f"{i} pokemons loaded.")

    return i


def search_pokemons(query, type):
    query = query.lower()
    pokemons = Pokemon.select().where(Pokemon.name.contains(query)).limit(20)

    if type is not None:
        filtered_pokemons = []
        for pokemon in pokemons:
            types = [t.type.name for t in pokemon.types]

            if type in types:
                filtered_pokemons.append(pokemon)
        return filtered_pokemons

    return pokemons


def edit_pokemon_stats(name, stat, new_value):
    pokemon = get_pokemon_by_name(name)

    update = {stat: new_value}
    pokemon.update(**update).execute()

    return pokemon


def delete_pokemon(name):
    pokemon = get_pokemon_by_name(name)
    pokemon.delete_instance(recursive=True)
    return True
