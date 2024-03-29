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
from typing import Optional

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import identifier_field, begin_field, end_field, \
  extension_field, stress_field, extensibility_field, ultimate_strength_field
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
  parser.add_argument('nb_points_smooth', type=int, nargs=1,
                      help="Number of points to use for running the "
                           "Savitzky-Golay filter for smoothening the second "
                           "derivative of the stress.")
  parser.add_argument('drop_threshold', type=float, nargs=1,
                      help="Minimum percentage of the total stress range in "
                           "the test above which a local drop in stress will "
                           "be considered as the end of the valid data.")
  parser.add_argument('nb_points_drop', type=int, nargs=1,
                      help="Length of the window over which to search for "
                           "drops in the stress value.")
  parser.add_argument('begin_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data on the "
                           "begin extensions.")
  parser.add_argument('maximum_point_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data on the "
                           "extrema points.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source_files = args.source_files
  begin_file = args.begin_file[0]
  max_file = args.maximum_point_file[0]
  nb_points_smooth = args.nb_points_smooth[0]
  drop_threshold = args.drop_threshold[0] / 100
  nb_points_drop = args.nb_points_drop[0]

  to_write: Optional[pd.DataFrame] = None

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)

  # Reading the begin points file and sorting the stress values
  begin = pd.read_csv(begin_file).sort_values(by=[identifier_field])
  begin_extensions = begin[begin_field]

  # Reading the max points file and sorting the stress values
  max_points = pd.read_csv(max_file).sort_values(by=[identifier_field])
  max_extensions = max_points[extensibility_field]
  max_stresses = max_points[ultimate_strength_field]

  # Iterating over the source files
  for path, extension, extensibility, max_stress in zip(source_files,
                                                        begin_extensions,
                                                        max_extensions,
                                                        max_stresses):
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)
    # Keeping only the valid data points
    data = data[(data[extension_field] >= extension) &
                (data[extension_field] <= extensibility)]

    # Searching for a sudden drop in the stress values
    max_index: Optional[int] = None
    for i in range(len(data) - nb_points_drop):
      # Iterating over sub-frames of the total series
      window = data[stress_field][i: i + nb_points_drop].values
      min_val = np.min(window)
      if window[0] - min_val > drop_threshold * max_stress:
        # Getting the maximum value reached before the stress drops
        (min_index, *_), *_ = np.where(window == min_val)
        (max_index, *_), *_ = np.where(window == np.max(window[:min_index]))
        max_index += i
        # Stopping as soon as the first drop is detected
        break

    # Excluding data after the drop in stress values, if one was detected
    if max_index is not None:
      data = data.iloc[:max_index]

    # Retrieving the first point where the second derivative cancels
    filtered = savgol_filter(data[stress_field].values, nb_points_smooth, 3,
                             deriv=2)
    cancel = np.diff(np.sign(filtered))
    if np.any(cancel):
      end = data[extension_field].values[np.argmin(cancel)]
    else:
      end = data[extension_field].max()

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame({identifier_field: [test_nr], end_field: [end]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr], end_field: [end]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
