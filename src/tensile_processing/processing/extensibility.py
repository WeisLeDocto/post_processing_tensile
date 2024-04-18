# coding: utf-8

"""This script reads stress-strain data from source files, determines for each
source file the extensibility, and saves the data at the provided location."""

import argparse
import pandas as pd
from typing import Optional

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import (identifier_field, extensibility_field,
                            extension_field, stress_field)
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # calculate max strain on data trimmed at the beginning

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="For each source file determines the extensibility, and then "
                "saves it in the destination file.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to store the "
                           "extensibility data.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source_files = args.source_files
  source_files = sorted(source_files, key=get_nr)

  # Creating the dataframe to save
  to_write: Optional[pd.DataFrame] = None

  # Iterating over the source files
  for path in source_files:
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)

    # Retrieving the extensibility
    index_max = data[stress_field].idxmax()
    extensibility = data[extension_field].iloc[index_max]

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame(
        {identifier_field: [test_nr], extensibility_field: [extensibility]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr], extensibility_field: [extensibility]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
