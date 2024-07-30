import os
import requests
from datetime import datetime, timedelta
from instagrapi import Client
import time

class InstagramDownloader:
    def __init__(self, username, password, target_username, output_folder='downloads', default_image_url=None, update_interval=60):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.output_folder = output_folder
        self.default_image_url = default_image_url
        self.update_interval = update_interval
        self.client = Client()
        self.logged_in = False

    def login(self):
        try:
            self.client.login(self.username, self.password)
            self.logged_in = True
            print("Login bem-sucedido")
        except Exception as e:
            print(f"Erro ao fazer login: {e}")

    def download_latest_image_posts(self, num_posts=4):
        if not self.logged_in:
            self.login()

        try:
            user_id = self.client.user_id_from_username(self.target_username)
            # Clear internal cache and force update user info to refresh data
            self.client.user_info_by_username(self.target_username)
            print(f"Página do usuário {self.target_username} recarregada")
            medias = self.client.user_medias(user_id, 100)  # Fetch more posts initially
        except Exception as e:
            print(f"Erro ao buscar mídias: {e}")
            return

        twenty_four_hours_ago = datetime.now() - timedelta(days=1)
        print(f"Fetching posts from the last 24 hours: {twenty_four_hours_ago}")

        image_posts = []
        for media in medias:
            media_date = datetime.fromtimestamp(media.taken_at.timestamp())
            if media_date < twenty_four_hours_ago:
                continue

            if media.media_type == 1:
                image_posts.append(media)
            elif media.media_type == 8:
                if all(item.media_type == 1 for item in media.resources):
                    image_posts.append(media)

        while len(image_posts) < num_posts:
            if self.default_image_url:
                image_posts.append(self.default_image_url)
            else:
                break

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        existing_files = set(os.listdir(self.output_folder))
        new_files = set()

        for i, media in enumerate(image_posts):
            if isinstance(media, str):
                filename = os.path.join(self.output_folder, f"default_{i}.jpg")
                if filename not in existing_files:
                    try:
                        response = requests.get(media)
                        if response.status_code == 200:
                            with open(filename, 'wb') as f:
                                f.write(response.content)
                            new_files.add(filename)
                            print(f"Downloaded and saved default image: {filename}")
                    except Exception as e:
                        print(f"Erro ao baixar imagem padrão: {e}")
            else:
                if media.media_type == 1:
                    image_url = media.thumbnail_url
                    filename = os.path.join(self.output_folder, f"{media.pk}.jpg")
                    if filename not in existing_files:
                        try:
                            response = requests.get(image_url)
                            if response.status_code == 200:
                                with open(filename, 'wb') as f:
                                    f.write(response.content)
                                new_files.add(filename)
                                print(f"Downloaded and saved image: {filename}")
                        except Exception as e:
                            print(f"Erro ao baixar imagem: {e}")
                elif media.media_type == 8:
                    for index, item in enumerate(media.resources):
                        if item.media_type == 1:
                            image_url = item.thumbnail_url
                            filename = os.path.join(self.output_folder, f"{media.pk}_{index}.jpg")
                            if filename not in existing_files:
                                try:
                                    response = requests.get(image_url)
                                    if response.status_code == 200:
                                        with open(filename, 'wb') as f:
                                            f.write(response.content)
                                        new_files.add(filename)
                                        print(f"Downloaded and saved carousel image: {filename}")
                                except Exception as e:
                                    print(f"Erro ao baixar imagem do carrossel: {e}")

        # Remove old files
        for file in existing_files:
            file_path = os.path.join(self.output_folder, file)
            if file_path not in new_files:
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

    def run(self):
        while True:
            try:
                self.download_latest_image_posts()
            except Exception as e:
                print(f"Erro no download de imagens: {e}")
            time.sleep(self.update_interval)

if __name__ == "__main__":
    username = 'ticavaleiro2'
    password = 'x45b150z'
    target_username = 'cavaleiroexpress'
    output_folder = 'downloads'
    default_image_url = 'https://example.com/default_image.jpg'
    update_interval = 60  # Intervalo de atualização em segundos (por exemplo, 60 segundos)

    downloader = InstagramDownloader(username, password, target_username, output_folder, default_image_url, update_interval)
    downloader.run()