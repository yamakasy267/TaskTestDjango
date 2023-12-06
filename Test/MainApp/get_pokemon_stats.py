import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from Test.settings import MEDIA_ROOT
import json
import dramatiq



@dramatiq.actor(max_age=36000000)
def get_pokemon_stats():
    response = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')
    with open(f'{MEDIA_ROOT}/pokemon.json', 'w', encoding='utf-8') as file:
        json.dump(response.json(), file)
