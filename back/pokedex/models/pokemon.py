from peewee import *
from playhouse.shortcuts import model_to_dict

from .database import db


class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = "public"


class Generation(CommonModel):
    id = PrimaryKeyField()
    name = CharField()


class Language(CommonModel):
    id = PrimaryKeyField()
    name = TextField()


class VerboseEffect(CommonModel):
    id = PrimaryKeyField()
    effect = TextField()
    short_effect = CharField()
    language = ForeignKeyField(Language)


class Pokemon(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    hp = FloatField()
    special_attack = FloatField()
    defense = FloatField()
    attack = FloatField()
    special_defense = FloatField()
    speed = FloatField()

    sprite_back = CharField(null=True)
    sprite_front = CharField(null=True)

    @property
    def stats(self):
        return {
            "hp": self.hp,
            "special-attack": self.special_attack,
            "defense": self.defense,
            "attack": self.attack,
            "special-defense": self.special_defense,
            "speed": self.speed,
        }

    def get_small_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "stats": self.stats,
            "sprite_back": self.sprite_back,
            "sprite_front": self.sprite_front,
        }


class Type(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    generation = ForeignKeyField(Generation)


class PokemonTypes(CommonModel):
    id = PrimaryKeyField()
    pokemon = ForeignKeyField(Pokemon)
    type = ForeignKeyField(Type, backref="pokemon_types")
    slot = IntegerField()


with db:
    Generation.create_table(fail_silently=True)
    Language.create_table(fail_silently=True)
    VerboseEffect.create_table(fail_silently=True)
    Pokemon.create_table(fail_silently=True)
    Type.create_table(fail_silently=True)
    PokemonTypes.create_table(fail_silently=True)
