# coding: utf-8

"""This script reads end-trimmed stress-strain data from source files, as well
as ultimate strengths from another file. It then determines for each source
file the minimum extension above which the stress-strain data is considered
valid, based either on a percentage of the maximum stress, or on a threshold on
the second derivative of the stress. The minimum extensions are finally saved
at the provided location."""

import argparse
import pandas as pd
from typing import Optional

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import identifier_field, begin_field, extension_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="For each source file, determines the minimum extension above "
                "which the stress-strain data is considered valid. The minimum"
                " extensions are then saved to the destination file.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to store the begin "
                           "extension data.")
  parser.add_argument('peak_prominence', type=float, nargs=1,
                      help="Minimum percentage of the total stress range in "
                           "the test above which a local stress peak will "
                           "be considered as the end of the valid data.")
  parser.add_argument('nb_points_peak', type=int, nargs=1,
                      help="Maximum width, in samples, of stress peaks to "
                           "consider for selecting the end cutoff extension.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source_files = args.source_files
  peak_prominence = args.peak_prominence[0] / 100
  nb_points_peak = args.nb_points_peak[0]

  # Creating the dataframe to save
  to_write: Optional[pd.DataFrame] = None

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)

  # Iterating over the source files
  for path in source_files:
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)

    # Just use the minimum extension, so this file is actually useless
    begin = data[extension_field].min()

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame({identifier_field: [test_nr],
                               begin_field: [begin]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr], begin_field: [begin]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
