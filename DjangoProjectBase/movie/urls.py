from django.urls import path
from .views import recommend_movie

urlpatterns = [
    path("recommend/", recommend_movie, name="recommend_movie"),
]
