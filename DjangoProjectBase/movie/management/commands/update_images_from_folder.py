import os
from django.core.management.base import BaseCommand
from movie.models import Movie
from django.conf import settings

class Command(BaseCommand):
    help = "Update movie images in the database from the media folder"

    def handle(self, *args, **kwargs):
        # 📂 Ruta de la carpeta donde están almacenadas las imágenes
        image_folder = os.path.join(settings.MEDIA_ROOT, 'movie', 'images')

        # ✅ Verifica si la carpeta existe
        if not os.path.exists(image_folder):
            self.stderr.write(f"Image folder '{image_folder}' not found.")
            return

        updated_count = 0

        # 🔄 Recorremos todas las películas en la base de datos
        for movie in Movie.objects.all():
            # 🏷️ Construimos el nombre esperado de la imagen
            image_filename = f"m_{movie.title}.png"
            image_path = os.path.join(image_folder, image_filename)

            if os.path.exists(image_path):
                # 📌 Guardamos solo la ruta relativa
                movie.image = f"movie/images/{image_filename}"
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title}")

        # ✅ Mensaje final con el total actualizado
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movie images."))
