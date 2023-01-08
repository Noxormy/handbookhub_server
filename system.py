from file_system import get_yaml_file


class FileNames:
    description: str = ""
    content: str = ""


class Config:
    data_folder: str = ""
    icon_name: str = ""
    file_names: FileNames = FileNames()

    def __init__(self, config_dict):
        assert isinstance(config_dict['data_folder'], str) and len(config_dict['data_folder']) > 0, "There is should be not empty data folder"
        self.data_folder = config_dict['data_folder']

        assert isinstance(config_dict['icon_name'], str) and config_dict['icon_name'].endswith('.png'), "There is should be icon in png format"
        self.icon_name = config_dict['icon_name']

        for name, file_name in config_dict['file_names'].items():
            assert hasattr(self.file_names, name), f"there is no file name: {name}"
            assert isinstance(file_name, str) and file_name.endswith('.md'), "File names should have .md extension"

            setattr(self.file_names, name, file_name)


config = Config(get_yaml_file('config.yml'))
