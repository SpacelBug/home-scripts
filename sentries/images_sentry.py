import os
import shutil

from PIL import Image

from sentries import explorer


class ImageFile(explorer.File):
    def __init__(self, path: str, name: str):
        super().__init__(path, name)

        self.resolution = self.info.split(',')[1]


def get_images_list(path):
    """
    Получение списка изображений в указанной директории path и всех ее дочерних директориях

    :param path путь к папке
    """
    images_list = []

    for file in explorer.Directory(path).get_all_files():
        if file.type.split('/')[0] == 'image':
            images_list.append(ImageFile(file.path, file.name))

    return images_list


def sort_images_by_param(from_path, to_path, param='resolution', copy=True):
    """
    Сортирует все изображения по папкам в соответствии с указанным параметром (по умолчанию - resolution)

    :param from_path из этой директории.
    :param to_path в эту директорию.
    :param param по данному параметру.
    :param copy если false то перемешает файлы а не копирует
    """
    images_list = get_images_list(from_path)

    if not os.path.exists(to_path):
        os.makedirs(to_path)

    for image in images_list:
        if hasattr(image, param):
            if not os.path.exists(f"{to_path}\\{getattr(image, param)}"):
                os.makedirs(f"{to_path}\\{getattr(image, param)}")
            if copy:
                shutil.copy2(image.path, f"{to_path}\\{getattr(image, param)}\\{image.name.replace(' ', '_')}")
            else:
                shutil.move(image.path, f"{to_path}\\{getattr(image, param)}\\{image.name.replace(' ', '_')}")

    return get_images_list(to_path)


def rename_images_with_numbers(path):
    """
    Переименовывает изображения нумеруя их по порядку
    """
    images_list = get_images_list(path)

    images_counter = 1

    for image in images_list:

        os.rename(
            image.path,
            image.path.replace(image.name, f"{images_counter}.{image.name.split('.')[len(image.name.split('.')) - 1]}")
        )

        images_counter += 1
