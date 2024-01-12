import magic
import os


class File:
    """
    Класс для файлов. Хранит путь к файлу, тип, информацию о нем и его название.

    :init path - путь к файлу.
    :init name - название файла.
    """
    def __init__(self, path: str, name: str):
        self.path = path
        self.type = magic.from_file(path, mime=True)
        self.info = magic.from_file(path)
        self.name = name


class Directory:

    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        self.name = os.path.basename(self.path)
        self.parent_path = os.path.dirname(self.path)

        files_params = []
        dirs_path = []

        with os.scandir(path) as list_of_entries:
            for entry in list_of_entries:
                if entry.is_file():
                    files_params.append({'path': entry.path, 'name': entry.name})
                else:
                    dirs_path.append(entry.path)

        self.files = self.__files_generator(files_params)
        self.dirs = self.__directories_genetator(dirs_path)

    def __files_generator(self, files: list):
        for file_params in files:
            yield File(**file_params)

    def __directories_genetator(self, dirs_path: list):
        for path in dirs_path:
            yield Directory(path)

    def navigate(self) -> None:

        while True:

            directories = [Directory(self.parent_path)] + [directory for directory in self.dirs]
            print(f"\nDirectories in '{self.name}':")

            counter = 0
            for directory in directories:
                print(f"    {counter}) '{directory.name}'")
                counter += 1

            try:
                selected_directory_index = int(input('Select dir by number (symbol will stop navigation) '))
            except ValueError as error:
                break

            if (selected_directory_index >= 0) and (selected_directory_index < len(directories)):
                self.__init__(directories[selected_directory_index].path)
            else:
                print('Wrong index!')
                self.__init__(self.path)
