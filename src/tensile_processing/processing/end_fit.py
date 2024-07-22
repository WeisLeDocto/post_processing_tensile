# coding: utf-8

"""This script reads trimmed stress-strain data from source files. It then
determines for each source file the maximum extension below which the
stress-strain data is considered valid for a Yeoh fit, based either on the
first cancellation point of the second derivative of stress or on the maximum
value of the first derivative of the stress. The maximum extensions are finally
saved at the provided location."""

import argparse
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter, find_peaks
from typing import Optional
from warnings import warn

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import (identifier_field, end_fit_field,
                            extension_field, stress_field,
                            ultimate_strength_field)
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="For each source file, determines the maximum extension under "
                "which the stress-strain data is considered valid for a fit "
                "with Yeoh. The maximum extensions are then saved to the "
                "destination file.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to store the end "
                           "extension data.")
  parser.add_argument('use_second_derivative', type=str, nargs=1,
                      help="Boolean indicating whether to use the second "
                           "derivative method for detecting the maximum "
                           "extension. Otherwise, the maximum of the first "
                           "derivative is used.")
  parser.add_argument('nb_points_smooth', type=int, nargs=1,
                      help="Number of points to use for running the "
                           "Savitzky-Golay filter for smoothening the first "
                           "or second derivative of the stress.")
  parser.add_argument('peak_prominence', type=float, nargs=1,
                      help="Minimum percentage of the total stress range in "
                           "the test above which a local stress peak will "
                           "be considered as the end of the valid data.")
  parser.add_argument('nb_points_peak', type=int, nargs=1,
                      help="Maximum width, in samples, of stress peaks to "
                           "consider for selecting the end cutoff extension.")
  parser.add_argument('ultimate_strength_file', type=checker_valid_csv,
                      nargs=1, help="Path to the .csv file containing the "
                                    "ultimate strength data.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source_files = args.source_files
  use_second_dev = True if args.use_second_derivative[0] == 'true' else False
  ultimate_strength_file = args.ultimate_strength_file[0]
  nb_points_smooth = args.nb_points_smooth[0]
  peak_prominence = args.peak_prominence[0] / 100
  nb_points_peak = args.nb_points_peak[0]

  to_write: Optional[pd.DataFrame] = None

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)

  # Reading the ultimate strength file and sorting the stress values
  ultimate_strength = pd.read_csv(ultimate_strength_file).sort_values(
    by=[identifier_field])
  max_stresses = ultimate_strength[ultimate_strength_field]

  # Iterating over the source files
  for path, max_stress in zip(source_files, max_stresses):
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)

    # Searching for a sudden drop in the stress values
    max_indices, _ = find_peaks(data[stress_field].values,
                                prominence=(peak_prominence * max_stress,
                                            None),
                                width=(None, nb_points_peak),
                                rel_height=1)

    # Excluding data after the drop in stress values, if one was detected
    if max_indices.size:
      data = data.iloc[:np.min(max_indices)]

    # In case the number of points for smoothening is greater than the number
    # of data points
    if nb_points_smooth > len(data):
      warn(f"Reduced the number of points from {nb_points_smooth} to "
           f"{int(len(data) / 2)} !", RuntimeWarning)
      nb_points_smooth = int(len(data) / 2)

    # Retrieving the first point where the second derivative cancels
    if use_second_dev:
      # The maximum extension is determined as the first cancellation point of
      # the second derivative of the stress
      filtered = savgol_filter(data[stress_field].values, nb_points_smooth, 3,
                               deriv=2)
      cancel = np.diff(np.sign(filtered))
      if np.any(cancel < 0):
        end = data[extension_field].values[np.min(np.where(cancel < 0))]
      else:
        end = data[extension_field].max()
    else:
      # The maximum extension is determined as the maximum of the first
      # derivative of the stress
      filtered = savgol_filter(data[stress_field].values, nb_points_smooth, 3,
                               deriv=1)
      end = data[extension_field].values[np.argmax(filtered)]

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame({identifier_field: [test_nr],
                               end_fit_field: [end]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr], end_fit_field: [end]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
