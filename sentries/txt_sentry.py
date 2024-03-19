import os

from sentries import explorer


def get_list_of_txt(path):
    """
    Возвращает список текстовых файлов
    """
    files_list = []

    for file in explorer.Directory(path).get_all_files():
        if file.type == 'text/plain':
            files_list.append(file)

    return files_list


def get_data_from_file(path):
    """
    Возвращает данные из файла
    """
    text_file = open(path)

    file_data = text_file.read()

    text_file.close()

    return file_data


def change_word_in_txt(path, target, new_value):
    """
    Меняет подстроку в файле

    :param path путь к файлу.
    :param target подстрока которую будем менять.
    :param new_value новое значение.
    """
    with open(path, "r") as text_file:

        old_file_data = text_file.read()

    new_file_data = old_file_data.replace(target, new_value)

    with open(path, "w") as text_file:

        text_file.write(new_file_data)
