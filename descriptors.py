import os
import re
from abc import ABC, abstractmethod


class AutoStorage:
    """Base for implementing descriptors"""

    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f"_{prefix}#{index}"
        cls.__counter += 1

    def __get__(self, instance, _):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""
        raise NotImplementedError


class Path(Validated):
    """a valid path (folder or file)"""

    def validate(self, instance, value):
        print(value)
        if not os.path.exists(value) and value is not None and value is not "":
            raise ValueError(f"Invalid file: {value}")
        return value


class File(Validated):
    """a valid file path"""

    def validate(self, instance, value):
        if not _is_valid_file(value) and value is not None and value is not "":
            raise ValueError(f"Invalid file: {value}")
        return value


class Folder(Validated):
    """a valid folder path"""

    def validate(self, instance, value):
        if not _is_valid_folder(value):
            raise ValueError(f"Invalid folder: {value}")
        return value


class Frequency(Validated):
    """a valid frequency"""

    def validate(self, instance, value):
        return _get_frequency_in_seconds(value)


class Required(Validated):
    """Raises ValueError if the value is falsy"""

    def validate(self, instance, value):
        if not value and value != 0:
            raise ValueError(f"Missing required or invalid property '{value}'")
        return value


def _is_valid_frequency(value: str) -> bool:
    """Returns true if the frequency passed is an instance of string, is not None, and adheres to the
    regex patterns for frequency strings.
    """
    pattern = r"^\d+[smhdwM]$"
    return isinstance(value, str) and re.match(pattern, value) is not None


def _get_frequency_in_seconds(value: str) -> int:
    """Converts a frequency string to seconds"""
    if not _is_valid_frequency(value):
        raise ValueError(f"Invalid frequency: {value}")
    measure = int(re.search(r"^\d+", value.strip().lower())[0])
    units = re.search(r"[a-z$]", value.strip().lower())[0]

    multiplier = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 60 * 60 * 24,
        "w": 60 * 60 * 24 * 7,
    }
    return measure * multiplier[units]


def _is_valid_file(path):
    """Returns True if path exists and is a file"""
    return os.path.exists(path) and os.path.isfile(path)


def _is_valid_folder(path):
    """Returns True if path exists and is a folder/directory"""
    return os.path.exists(path) and os.path.isdir(path)


def _is_empty(value):
    """Returns true if value is none or empty string"""
    return value is None or value is ""


if __name__ == "__main__":
    pass
