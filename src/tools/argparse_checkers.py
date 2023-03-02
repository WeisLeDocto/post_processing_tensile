# coding: utf-8

"""This file contains the checkers for checking the command-line arguments of
the executable Python scripts."""

import argparse
from pathlib import Path


def checker_valid_csv(raw_path: str) -> Path:
  """Function checking that the provided path to the .csv file is valid.

  Args:
    raw_path: The provided path, as a string.

  Returns:
    The pathlib Path associated with the provided string path.

  Raises:
    argparse.ArgumentTypeError: Raised in case the provided path does not
      exist, or if it is not a file, or if the file extension is not .csv.
  """

  path = Path(raw_path)
  if not path.suffix == '.csv':
    raise argparse.ArgumentTypeError(f'The extension of the provided file '
                                     f'should be .csv, got {path.suffix} for '
                                     f'file {str(path)}')
  elif not path.exists():
    raise argparse.ArgumentTypeError(f"The file {str(path)} does not exist !")
  elif not path.is_file():
    raise argparse.ArgumentTypeError(f"The path {str(path)} does not point to "
                                     f"a file !")
  return path


def checker_is_tiff(raw_path: str) -> Path:
  """Function checking that the provided path to the .tiff file is valid.

  Args:
    raw_path: The provided path, as a string.

  Returns:
    The pathlib Path associated with the provided string path.

  Raises:
    argparse.ArgumentTypeError: Raised in case the file extension is not .tiff.
  """

  path = Path(raw_path)
  if not path.suffix == '.tiff':
    raise argparse.ArgumentTypeError(f'The extension of the provided file '
                                     f'should be .tiff, got {path.suffix} for '
                                     f'file {str(path)}')
  return path


def checker_is_csv(raw_path: str) -> Path:
  """Function checking that the provided path to the .csv file is valid.

  Args:
    raw_path: The provided path, as a string.

  Returns:
    The pathlib Path associated with the provided string path.

  Raises:
    argparse.ArgumentTypeError: Raised in case the file extension is not .csv.
  """

  path = Path(raw_path)
  if not path.suffix == '.csv':
    raise argparse.ArgumentTypeError(f'The extension of the provided file '
                                     f'should be .csv, got {path.suffix} for '
                                     f'file {str(path)}')
  return path
