import os

from PIL import Image


def sort_images_by_resolution(from_path='.', to_path='.'):

    images_list = []

    for path, directories, file_names in os.walk(from_path):
        for file_name in file_names:
            try:
                image = Image.open(f'{path}\{file_name}')
                image_resolution = f'{image.size[0]}-{image.size[1]}'
                images_list.append({
                    'path': f'{os.getcwd()}\{path}\{file_name}',
                    'name': file_name,
                    'resolution': image_resolution,
                })
                image.close()
            except Exception as error:
                print(f"Error with file  '{file_name}' - {error}")

    if not os.path.exists(to_path):
        os.makedirs(to_path)

    for image in images_list:
        if not os.path.exists(image.get('resolution')):
            os.makedirs(image.get('resolution'))
        os.rename(image.get('path'), f"{to_path}\\{image.get('resolution')}\\{image.get('name')}")