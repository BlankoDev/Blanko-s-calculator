from json import load, dumps
from os import path
from typing import Callable
from libs.translation import get_id_from_name


class Configuration(object):
    def __init__(self, file_path, default: dict):
        if path.exists(file_path):
            self.file_path = file_path
            self._json_file = open(file_path, "r")
            self.json = load(self._json_file)
        else:

            self._json_file = open(file_path, "w")
            self._json_file.write(dumps(default))

            self.json = default

    def get(self, option_name: str):
        return self.json[option_name]

    def set(self, option_name: str, value):
        tmp = open(self.file_path, "w")
        self.json[option_name] = value
        
        tmp.write(dumps(self.json))
        tmp.close()

    def close(self):
        self._json_file.close()
    
    def __str__(self) -> str:
        return str(self.json)


class Option(object):
    def __init__(self, key, parent_config_file, validation_command: Callable, option_id : str | None = None):
        self.validation_command = validation_command

        self.id = option_id
        self._parent_config_file = parent_config_file
        self._key = key
        self._value = parent_config_file[key]
        self.type = type(self._value)

    def set(self, value):
        self.type = type(value)
        self._parent_config_file[self._key] = value

    def get(self):
        return self._parent_config_file[self._key]
    
    def get_id(self):
        return self.id

    def validate(self):
        self.validation_command(self._key)

    def __str__(self):
        return str(self._parent_config_file[self._key])


class CalculatorConfig(Configuration):
    def __init__(self):
        default = {
            "lang": "system",
            "theme": "system",
            "hide_delay": 0.3
        }

        super().__init__("config.json", default)

        self.LANG = Option("lang", self.json, self._write_to_file, get_id_from_name(self.json["lang"]))
        self.THEME = Option("theme", self.json, self._write_to_file)
        self.HIDE_DELAY = Option("hide_delay", self.json, self._write_to_file)
    def _write_to_file(self, key):
        self.set(key, self[key])
    def __setitem__(self, key: str, value):
        if not isinstance(key, str):
            raise TypeError(f"invalid type {type(key)}")
        if key.lower() == "lang":
            self.LANG.set(value)
            self.LANG.validate()
        if key.lower() == "theme":
            self.THEME.set(value)
            self.THEME.validate()
        if key.lower() == "hide_delay":
            self.HIDE_DELAY.set(value)
            self.HIDE_DELAY.validate()

    def __getitem__(self, key: str):
        if not isinstance(key, str):
            raise TypeError(f"invalid type {type(key)}")
        if key.lower() == "lang":
            return self.LANG.get()
        if key.lower() == "theme":
            return self.THEME.get()
        if key.lower() == "hide_delay":
            return self.HIDE_DELAY.get()
