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
from scipy.signal import savgol_filter
from warnings import warn

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import (identifier_field, begin_field, extension_field,
                            stress_field)
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
  parser.add_argument('use_second_derivative', type=str, nargs=1,
                      help="Boolean indicating whether to use the second "
                           "derivative method for detecting the minimum "
                           "extension. Otherwise, the stress threshold method "
                           "is used.")
  parser.add_argument('stress_threshold', type=float, nargs=1,
                      help="The percentage of the total stress below which the"
                           " data is not considered valid. Only used with the "
                           "stress threshold method.")
  parser.add_argument('nb_points_smooth', type=int, nargs=1,
                      help="Number of points to use for running the "
                           "Savitzky-Golay filter for smoothening the second "
                           "derivative of the stress, if the second derivative"
                           " method is used. Only used with the second "
                           "derivative method.")
  parser.add_argument('second_derivative_threshold', type=float, nargs=1,
                      help="The percentage of the maximum second derivative "
                           "value below which the data is not considered "
                           "valid. Only used with the second derivative "
                           "method.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  use_second_dev = True if args.use_second_derivative[0] == 'true' else False
  nb_points_smooth = args.nb_points_smooth[0]
  sec_dev_thresh = args.second_derivative_threshold[0] / 100
  source_files = args.source_files
  threshold = args.stress_threshold[0] / 100

  # Creating the dataframe to save
  to_write: Optional[pd.DataFrame] = None

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)

  # Iterating over the source files
  for path in source_files:
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)

    # Restricting data to the portion of interest
    idx_max = data[stress_field].idxmax()
    idx_min = data.iloc[:idx_max][stress_field].idxmin()
    data = data.iloc[idx_min: idx_max]

    # Determining the beginning point of the valid data based on the value of
    # the second derivative
    if use_second_dev:

      if nb_points_smooth > len(data):
        warn(f"Reduced the number of points from {nb_points_smooth} to "
             f"{int(len(data) / 10)} !", RuntimeWarning)
        nb_points_smooth = int(len(data) / 10)

      sec_dev = savgol_filter(data[stress_field].values, nb_points_smooth, 3,
                              deriv=2)
      begin = data[extension_field][sec_dev >
                                    sec_dev_thresh * sec_dev.max()].min()

    # Determining the beginning point of the valid data based on a stress
    # threshold
    else:
      stress_amp = data[stress_field].max() - data[stress_field].min()
      begin = data[extension_field][data[stress_field] >
                                    threshold * stress_amp].min()

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame({identifier_field: [test_nr],
                               begin_field: [begin]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr], begin_field: [begin]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
