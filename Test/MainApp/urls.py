from django.urls import re_path
from .views import *
from .get_pokemon_stats import get_pokemon_stats

urlpatterns = [
    re_path(r'^registration/', Registration.as_view(), name='registration'),
    re_path(r'^login/', Login.as_view(), name='login'),
    re_path(r'^upload_file/', UploadFile.as_view(), name='upload_file'),
    re_path(r'^get_file/', GetFile.as_view(), name='get_file'),
    re_path(r'^delete_file/', DeleteFile.as_view(), name='delete_file'),
    re_path(r'^update_file/', UpdateFile.as_view(), name='update_file'),
]
get_pokemon_stats.send()