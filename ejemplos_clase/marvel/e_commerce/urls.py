from django.urls import path
from e_commerce.marvel_views import *


urlpatterns = [
    path('get-comics/', get_comics),
    path('purchased-item/', purchased_item),
]
