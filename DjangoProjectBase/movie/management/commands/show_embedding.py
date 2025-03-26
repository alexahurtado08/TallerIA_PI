import random
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Muestra los embeddings de una película seleccionada al azar"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()

        if not movies:
            self.stdout.write(self.style.ERROR("No hay películas en la base de datos."))
            return

        # Seleccionar una película al azar
        movie = random.choice(movies)
        embeddings = np.frombuffer(movie.emb, dtype=np.float32)  # Convertir de bytes a array

        self.stdout.write(self.style.SUCCESS(f"Película seleccionada: {movie.title}"))
        self.stdout.write(self.style.SUCCESS(f"Embeddings: {embeddings}"))
