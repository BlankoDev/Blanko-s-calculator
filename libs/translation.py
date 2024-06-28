from json import load, dump
from locale import getdefaultlocale
from os import listdir

TRANSLATION_KEYS = [
    "TITLE", "SETTINGS_TITLE", "LANGUAGE_OPTION_TEXT", "LANGUAGE_INFO", "THEME_OPTION_TEXT", "THEME_INFO", "THEME_MENU_VALUE", "HIDE_DELAY_OPTION_TEXT",
    "HIDE_DELAY_INFO", "CREDITS", "RELEASE_NOTE", "GO_TO_GITHUB", "PYTHON_VERSION", "APP_VERSION", "ABOUT", "VERSION", "DEVELOPER", "ABOUT_ICON",
    "SETTINGS_ICON", "BACK_ICON", "alias", "encoding"
    ]
TRANSLATION_KEYS.sort()


class Language(object):
    def __init__(self):
        
        tmp_languages = {}
        tmp_languages_alias = []
        index_file = open("lang/index.json", "w", encoding="utf-8")
        index_json = {}

        for language_file in listdir("lang"):
            if language_file == "index.json":
                continue
            tmp_file = open(f"lang/{language_file}", encoding="utf-8")
            tmp = load(tmp_file)
            tmp_file.close()
            name = language_file.removesuffix(".bcl")
            index_json[tmp["alias"]] = {"id": name, "encoding": tmp["encoding"]}

            tmp_languages[name] = tmp["alias"]
            tmp_languages_alias.append(tmp["alias"])
        dump(index_json, index_file)
        index_file.close()
        tmp_languages_alias.append("system")
        self.languages = tmp_languages
        self.languages_alias = tmp_languages_alias

        self.language = getdefaultlocale()[0]

    def set_language(self, lang_id: str = "system"):
        if lang_id == "system":
            file_name = f"{self.language}.bcl"
            file_path = f"lang/{file_name}"
            lang_id = self.language
            
        else:
            file_name = f"{lang_id}.bcl"
            file_path = f"lang/{file_name}"

        if file_name not in listdir("lang"):
            file_path = "lang/en_US.bcl"


        index_file = open("lang/index.json", "r", encoding="utf-8")
        index_json = load(index_file)[self.languages[lang_id]]
        index_file.close()

        _json_file = open(file_path, encoding=index_json["encoding"])
        self.json_dict = load(_json_file)

        self.TITLE = self.json_dict["TITLE"]
        self.SETTINGS_TITLE = self.json_dict["SETTINGS_TITLE"]

        self.LANGUAGE_OPTION_TEXT = self.json_dict["LANGUAGE_OPTION_TEXT"]
        self.LANGUAGE_INFO = self.json_dict["LANGUAGE_INFO"]

        self.THEME_OPTION_TEXT = self.json_dict["THEME_OPTION_TEXT"]
        self.THEME_INFO = self.json_dict["THEME_INFO"]
        self.THEME_MENU_VALUE = self.json_dict["THEME_MENU_VALUE"]

        self.HIDE_DELAY_OPTION_TEXT = self.json_dict["HIDE_DELAY_OPTION_TEXT"]
        self.HIDE_DELAY_INFO = self.json_dict["HIDE_DELAY_INFO"]
        self.CREDITS = self.json_dict["CREDITS"]
        self.RELEASE_NOTE = self.json_dict["RELEASE_NOTE"]
        self.GO_TO_GITHUB = self.json_dict["GO_TO_GITHUB"]
        self.PYTHON_VERSION = self.json_dict["PYTHON_VERSION"]
        self.APP_VERSION = self.json_dict["APP_VERSION"]

        self.ABOUT = self.json_dict["ABOUT"]
        self.VERSION = self.json_dict["VERSION"]
        self.DEVELOPER = self.json_dict["DEVELOPER"]
        self.ABOUT_ICON = self.json_dict["ABOUT_ICON"]

        self.SETTINGS_ICON = self.json_dict["SETTINGS_ICON"]
        self.BACK_ICON = self.json_dict["BACK_ICON"]



def check_validity(json_obj):
    dic = list(json_obj.keys())
    dic.sort()
    return dic == TRANSLATION_KEYS


def get_id_from_name(name : str):
    if name == "system":
        return name
    index_file = open("lang/index.json", "r", encoding="utf-8")
    index_json = load(index_file)
    index_file.close()
    return index_json[name]["id"]
    

