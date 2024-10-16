import os
import shutil

from PIL import Image, ImageChops

import piexif

from sentries import explorer


class ImageFile(explorer.File):
    def __init__(self, path: str, name: str):
        super().__init__(path, name)

        with Image.open(self.path) as image:
            self.resolution = 'x'.join([str(value) for value in image.size])

    def get_info(self):

        with Image.open(self.path) as image:
            return image.info

    def get_exif(self):
        """
        Возвращает словарь exif изображения.
        Return dict of image exif.
        """
        with Image.open(self.path) as img:
            exif_data = piexif.load(img.info["exif"])

            decode_exif = {}

            for tag, value in exif_data['Exif'].items():
                decode_exif[tag] = value.decode('utf-16', errors='ignore')

            return decode_exif

    def add_tags_to_image(self, tags: list):
        """
        Записывает тэги в поле UserComment в exif изображения.
        Put tags into image exif`s UserComment tag.

        :param tags: list of tags
        """

        image = Image.open(self.path)

        exif_dict = piexif.load(image.info['exif'])

        tags_string = ', '.join(tags)

        exif_dict['Exif'][piexif.ExifIFD.UserComment] = tags_string.encode('utf-16')

        exif_bytes = piexif.dump(exif_dict)
        image.save(self.path, exif=exif_bytes)


def get_images_list(path):
    """
    Получение списка изображений в указанной директории path и всех ее дочерних директориях

    :param path путь к папке
    """
    images_list = []

    for file in explorer.Directory(path).get_all_files():
        if file.extension in ['png', 'jpg', 'jpeg']:
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


def image_pixel_differences(base_image: ImageFile, compare_image: ImageFile) -> bool:
    """
    Сравнивает два изображения
    """
    if base_image.resolution == compare_image.resolution:
        diff = ImageChops.difference(Image.open(base_image.path), Image.open(compare_image.path))

        if diff.getbbox():
            return False
        else:
            return True
    else:
        return False


def find_image_clones(path):
    """
    Ищет все копии изображений в указанной директории
    """
    images = get_images_list(path)

    cache = []
    result = {}

    for first_image in images:
        first_image_copies = []
        for second_image in images:
            if first_image.path != second_image.path:
                if first_image.path not in cache:
                    if image_pixel_differences(first_image, second_image):
                        cache.append(second_image.path)
                        first_image_copies.append(second_image.path)
        if first_image_copies:
            result[first_image.path] = first_image_copies

    return result