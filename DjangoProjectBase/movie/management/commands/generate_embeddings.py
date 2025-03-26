import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Generate and store embeddings for all movies"

    def handle(self, *args, **kwargs):
        # Cargar API key
        load_dotenv('openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        # Función auxiliar para obtener embeddings
        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        # Procesar cada película
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            try:
                emb = get_embedding(movie.description)  # Generar embedding
                movie.emb = emb.tobytes()  # Guardar como binario
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Stored embedding for: {movie.title}"))
            except Exception as e:
                self.stderr.write(f"Failed to process {movie.title}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Finished generating embeddings for all movies"))
