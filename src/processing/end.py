# coding: utf-8

"""This script reads stress-strain data from source files, as well as begin
extensions from another file. It then determines for each source file the
maximum extension below which the stress-strain data is considered valid, based
on the first cancellation point of the second derivative of stress. The maximum
extensions are finally saved at the provided location."""

import argparse
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import identifier_field, begin_field, end_field, \
  extension_field, stress_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="For each source file, determines the maximum extension under "
                "which the stress-strain data is considered valid. The maximum"
                " extensions are then saved to the destination file.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to store the end "
                           "extension data.")
  parser.add_argument('nb_points', type=int, nargs=1,
                      help="Number of points to use for running the "
                           "Savitzky-Golay filter for smoothening the second "
                           "derivative.")
  parser.add_argument('begin_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data on the "
                           "begin extensions.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source_files = args.source_files
  begin_file = args.begin_file[0]
  nb_points = args.nb_points[0]

  # Creating the dataframe to save
  to_write = pd.DataFrame(columns=[identifier_field, end_field])

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)

  # Reading the max points file and sorting the stress values
  begin = pd.read_csv(begin_file).sort_values(by=[identifier_field])
  begin_extensions = begin[begin_field]

  # Iterating over the source files
  for path, extension in zip(source_files, begin_extensions):
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)
    # Keeping only the valid data points
    data = data[data[extension_field] >= extension]

    # Retrieving the first point where the second derivative cancels and the
    # first derivative is zero
    filtered = savgol_filter(data[stress_field].values, nb_points, 3, deriv=1)
    end = data[extension_field].values[np.argmax(filtered)]

    # Adding the values to the dataframe to save
    to_write = pd.concat((to_write, pd.DataFrame({identifier_field: [test_nr],
                                                  end_field: [end]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
