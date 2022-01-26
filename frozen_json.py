import json
import keyword
import os
from collections import abc
from io import TextIOWrapper


class FrozenJSON:
    """Read only facade for navigating a JSON like object using attribute notation"""

    @classmethod
    def __new__(cls, *args, **kwargs):
        if isinstance(args[1], abc.Mapping):
            return super().__new__(cls)
        elif isinstance(args[1], abc.MutableSequence):
            return [cls(item) for item in args[1]]
        else:
            return args[1]

    def __init__(self, mapping):
        self._data = {}
        for key, value in mapping.items():
            self._data[self.validate_identifier(key)] = value

    def __getattr__(self, name):
        if name in self._data:
            return FrozenJSON(self._data[name])
        raise AttributeError(f"Not found: {name}")

    @classmethod
    def validate_identifier(cls, identifier: str):
        idx = 0

        def validated(__identifier):
            validated_identifier = __identifier
            # handle identifier is a Python keyword
            if keyword.iskeyword(__identifier):
                __identifier += "_"
            # handle identifier starts with an integer
            if __identifier[0].isdigit():
                __identifier = f"{str(chr(idx))}_{validated_identifier[1:]}"
            if not __identifier.isidentifier():
                raise ValueError(f"Could not create valid key from: {__identifier}")
            return __identifier

        return validated(identifier)

    @classmethod
    def of(cls, data):
        __map = {
            "str": cls.from_string,
            "dict": cls.from_mapping,
            "TextIOWrapper": cls.from_file,
            "object": lambda x: None,
        }
        return __map[data.__class__.__name__](data)

    @classmethod
    def from_string(cls, json_string):
        if is_valid_file_path(json_string):
            return cls.from_file_path(json_string)
        return cls(json.loads(json_string))

    @classmethod
    def from_mapping(cls, mapping):
        return cls(mapping)

    @classmethod
    def from_file_path(cls, absolute_path):
        with open(absolute_path) as json_file:
            json_data = json.load(json_file)
            return cls(json_data)

    @classmethod
    def from_file(cls, _file: TextIOWrapper):
        data = json.load(_file)
        return cls(data)


def is_valid_file_path(value):
    return os.path.exists(value) and os.path.isfile(value)
