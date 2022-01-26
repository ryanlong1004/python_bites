import os
import shutil
import time
from typing import Iterator

import pytest
from py._path.local import LocalPath


@pytest.fixture
def here() -> str:
    """Returns the absoluate path of the project root
    Returns:
        str: path
    """
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def create_file(tmpdir: LocalPath) -> Iterator[str]:
    """Creates a random file for testing in the tmpdir fixture
    Yields:
        Iterator[TextIOWrapper]: file instance
    """
    folder: LocalPath = tmpdir.mkdir(random_name())
    file: str = folder.join(random_name())
    with open(file, "w") as _file:
        yield _file.name
    shutil.rmtree(folder)


@pytest.fixture
def create_folder(tmpdir: LocalPath) -> Iterator[LocalPath]:
    """Creates a random folder in temp for testing in the tmpdir fixture
    Yields:
        Iterator[LocalPath]: folder instance
    """

    folder: LocalPath = tmpdir.mkdir(random_name())
    yield folder
    shutil.rmtree(folder)


def random_name() -> str:
    """Returns a random string of ints based on the current time
    Returns:
        str: random string
    """
    return str(int(time.time()))


def get_abs_path(relative_path: str) -> str:
    """Attempts to return the absolute path of a relative path
    by joining the relative path with the project root
    Args:
        relative_path (str): the relative path
    Returns:
        str: the absolute path
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(project_root, relative_path)
