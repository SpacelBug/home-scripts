import os

from PIL import Image


def get_images_list(path):

    images_list = []

    for path, directories, file_names in os.walk(path):
        for file_name in file_names:
            try:
                image = Image.open(f'{path}\{file_name}')
                image_resolution = f'{image.size[0]}-{image.size[1]}'
                images_list.append({
                    'path': f'{os.getcwd()}\{path}\{file_name}',
                    'name': file_name,
                    'resolution': image_resolution,
                    'extension': file_name.split('.')[len(file_name.split('.'))-1]
                })
                image.close()
            except Exception as error:
                print(f"Error with file  '{file_name}' - {error}")

    return images_list


def sort_images_by_param(from_path='.', to_path='.', param='resolution'):

    images_list = get_images_list(from_path)

    if not os.path.exists(to_path):
        os.makedirs(to_path)

    for image in images_list:
        if not os.path.exists(image.get(param)):
            os.makedirs(image.get(param))
        os.rename(image.get('path'), f"{to_path}\\{image.get(param)}\\{image.get('name')}")

    return get_images_list(to_path)