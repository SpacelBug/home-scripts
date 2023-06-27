import os
from .images_sentry import get_images_list


def create_captions(path, default_caption=None):
    for file in get_images_list(path):
        os.chdir(path)
        with open(f"{path}/{file.name.split('.')[0]}.txt", 'a+') as caption_file:
            try:
                caption_file.write(default_caption)
            except FileNotFoundError:
                print(f'File not found: path="{path}/{file.name}"')
