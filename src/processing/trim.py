# coding: utf-8

"""This script reads stress-strain data from the source file, as well as the
beginning and end extension from another file. It then trims the stress-strain
data according to the beginning and end extensions, and saves the trimmed data
at the provided location."""

import argparse
import pandas as pd

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import identifier_field, begin_field, end_field, \
  extension_field, stress_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Reads the stress-strain data from the source files, as well "
                "as the begin and end extension values. Then, trims the "
                "stress-strain data according to the begin and end extensions "
                "and saves the trimmed data in the destination file.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to save the trimmed "
                           "stress-strain data.")
  parser.add_argument('source_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv files containing the "
                           "stress-strain data.")
  parser.add_argument('begin_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the begin "
                           "extension data.")
  parser.add_argument('end_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the end "
                           "extension data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source = args.source_file[0]
  begin_file = args.begin_file[0]
  end_file = args.end_file[0]

  # Loading data from the source file
  test_nr = get_nr(source)
  data = pd.read_csv(source)

  # Reading the beginning and end extensions from the data files
  begin = pd.read_csv(begin_file)
  begin = float(begin[begin_field][begin[identifier_field] == test_nr])
  end = pd.read_csv(end_file)
  end = float(end[end_field][end[identifier_field] == test_nr])

  # Keeping only the valid data and offsetting the extension and the stress
  valid = data[(data[extension_field] >= begin) &
               (data[extension_field] <= end)]
  valid /= [valid[extension_field].iloc[0], 1]
  valid -= [0, valid[stress_field].iloc[0]]

  # Saving the values to the destination file
  valid.to_csv(destination, index=False)
