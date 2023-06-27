import os
from .images_sentry import get_images_list


def create_captions(path, default_caption=''):
    for file in get_images_list(path):
        os.chdir(path)
        if file.get('name'):
            with open(f"{path}/{file.get('name').split('.')[0]}.txt", 'w+') as caption_file:
                try:
                    caption_file.write(default_caption)
                except FileNotFoundError:
                    print(f'File not found: path="{path}/{file.name}"')
