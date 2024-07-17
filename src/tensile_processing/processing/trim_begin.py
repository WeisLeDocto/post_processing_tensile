# coding: utf-8

"""This script reads end-trimmed stress-strain data from the source file, as
well as the begin cutoff extension from another file. It then trims the
beginning of the stress-strain data, and saves the trimmed data at the provided
location."""

import argparse
import pandas as pd

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import (identifier_field, begin_field, extension_field,
                            stress_field)
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Reads the begin-trimmed stress-strain data from the source "
                "files, as well as the begin cutoff extension values. Then, "
                "trims the beginning of the stress-strain data and saves the "
                "trimmed data in the destination file.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to save the trimmed "
                           "stress-strain data.")
  parser.add_argument('source_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv files containing the end-trimmed"
                           "stress-strain data.")
  parser.add_argument('begin_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the begin cutoff "
                           "extension values.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source = args.source_file[0]
  begin_file = args.begin_file[0]

  # Loading data from the source file
  test_nr = get_nr(source)
  data = pd.read_csv(source)

  # Reading the beginning from the data files
  begin = pd.read_csv(begin_file)
  begin = float(begin[begin_field][begin[identifier_field] == test_nr].iloc[0])

  # Keeping only the valid data and offsetting the extension and the stress
  valid = data[data[extension_field] >= begin]
  valid /= [valid[extension_field].iloc[0], 1]
  valid -= [0, valid[stress_field].iloc[0]]

  # Saving the values to the destination file
  valid.to_csv(destination, index=False)
