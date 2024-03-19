import os
import shutil

from PIL import Image


def get_images_list(path):
    """
    Получение списка изображений в указанной директории path и всех ее дочерних директориях

    :param path путь к папке
    """
    images_list = []

    for path, directories, file_names in os.walk(path):
        for file_name in file_names:
            try:
                image = Image.open(f'{path}\{file_name}')
                image_resolution = f'{image.size[0]}-{image.size[1]}'
                images_list.append({
                    'path': f'{path}\{file_name}',
                    'name': file_name,
                    'resolution': image_resolution,
                    'extension': file_name.split('.')[len(file_name.split('.'))-1]
                })
                image.close()
            except Exception as error:
                print(f"Error with file  '{file_name}' - {error}")

    return images_list


def sort_images_by_param(from_path, to_path, param='resolution', copy=True):
    """
    Сортирует все изображения по папкам в соответствии с указанным параметром (по умолчанию - resolution)

    :param from_path из этой директории.
    :param to_path в эту директорию.
    :param param по данному параметру.
    """
    images_list = get_images_list(from_path)

    if not os.path.exists(to_path):
        os.makedirs(to_path)

    for image in images_list:
        if not os.path.exists(f"{to_path}\\{image.get(param)}"):
            os.makedirs(f"{to_path}\\{image.get(param)}")
        if copy:
            shutil.copy2(image.get('path'), f"{to_path}\\{image.get(param)}\\{image.get('name').replace(' ', '_')}")
        else:
            shutil.move(image.get('path'), f"{to_path}\\{image.get(param)}\\{image.get('name').replace(' ', '_')}")

    return get_images_list(to_path)


def rename_images_with_numbers(path):
    """
    Переименовывает изображения нумеруя их по порядку
    """
    images_list = get_images_list(path)

    images_counter = 1

    for image in images_list:

        os.rename(
            image.get('path'),
            image.get('path').replace(image.get('name'), f"{images_counter}.{image.get('extension')}")
        )

        images_counter += 1
