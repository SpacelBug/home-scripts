import os


def get_list_of_txt(path):
    files_list = []

    for path, directories, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.split('.')[1] == 'txt':
                files_list.append(f'{path}\\{file_name}')

    return files_list


def get_data_from_file(path):

    file = open(path)

    print(file.read())


def change_word_in_txt(path, target, new_value):

    text_file = open(path, "r")

    file_data = text_file.read()

    file_data = file_data.replace(target, new_value)

    text_file.close()

    text_file = open(path, "w")

    text_file.write(file_data)

    text_file.close()


path = f'C:\\Users\\PKompik\\Desktop\\git\\home-scripts\\test_data\\50_morkovochka'

for file in (get_list_of_txt(path)):
    change_word_in_txt(file, 'girl, ', '')
