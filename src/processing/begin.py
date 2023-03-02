# coding: utf-8

"""This script reads stress-strain data from source files, as well as ultimate
strengths from another file. It then determines for each source file the
minimum extension above which the stress-strain data is considered valid, based
on a percentage of the ultimate strength. The minimum extensions are finally
saved at the provided location."""

import argparse
import pandas as pd

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import identifier_field, begin_field, \
  ultimate_strength_field, extension_field, stress_field
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
  parser.add_argument('stress_threshold', type=float, nargs=1,
                      help="The percentage of the total stress below which the"
                           " data is not considered valid.")
  parser.add_argument('max_points_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the ultimate "
                           "strength and the extensibility.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source_files = args.source_files
  threshold = args.stress_threshold[0] / 100
  max_points_file = args.max_points_file[0]

  # Creating the dataframe to save
  to_write = pd.DataFrame(columns=[identifier_field, begin_field])

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)
  # Reading the max points file and sorting the stress values
  max_points = pd.read_csv(max_points_file).sort_values(by=[identifier_field])
  max_stresses = max_points[ultimate_strength_field]

  # Iterating over the source files
  for path, max_stress in zip(source_files, max_stresses):
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)

    # Determining the beginning point of the valid data
    begin = data[extension_field][data[stress_field] >
                                  threshold * max_stress].min()
    # Adding the values to the dataframe to save
    to_write = pd.concat((to_write, pd.DataFrame({identifier_field: [test_nr],
                                                  begin_field: [begin]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
