import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
import random

class Command(BaseCommand):
    help = "View embeddings of a random movie"

    def handle(self, *args, **kwargs):
        movies = list(Movie.objects.all())
        if not movies:
            self.stdout.write("No movies found in the database.")
            return

        movie = random.choice(movies)
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)

        self.stdout.write(f"Movie: {movie.title}")
        self.stdout.write(f"Embedding (first 5 values): {embedding_vector[:5]}")
