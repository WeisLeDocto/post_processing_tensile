# coding: utf-8

"""This file contains a function for parsing a path and extracting the test
number from it."""

from re import findall
from pathlib import Path


def get_nr(path: Path) -> int:
  """Returns the test number from the given path."""

  return int(findall(r'\d+', path.stem)[0])
