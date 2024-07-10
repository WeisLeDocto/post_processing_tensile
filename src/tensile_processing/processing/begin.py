# coding: utf-8

"""This script reads stress-strain data from source files, as well as ultimate
strengths from another file. It then determines for each source file the
minimum extension above which the stress-strain data is considered valid, based
either on a percentage of the ultimate strength, or on a threshold on the
second derivative of the stress. The minimum extensions are finally saved at
the provided location."""

import argparse
import pandas as pd
from typing import Optional
from scipy.signal import savgol_filter

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
  parser.add_argument('ultimate_strength_file', type=checker_valid_csv,
                      nargs=1, help="Path to the .csv file containing the "
                                    "ultimate strength.")
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
  ultimate_strength_file = args.ultimate_strength_file[0]

  # Creating the dataframe to save
  to_write: Optional[pd.DataFrame] = None

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)
  # Reading the max points file and sorting the stress values
  ultimate_strength = pd.read_csv(ultimate_strength_file).sort_values(
    by=[identifier_field])
  max_stresses = ultimate_strength[ultimate_strength_field]

  # Iterating over the source files
  for path, max_stress in zip(source_files, max_stresses):
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)

    # Determining the beginning point of the valid data based on the value of
    # the second derivative
    if use_second_dev:
      ext_max = data[extension_field].where(
        data[stress_field] == max_stress).min()
      filtered_stress = savgol_filter(
        data[stress_field].values, nb_points_smooth, 3,
        deriv=2)[data[extension_field] <= ext_max]
      filtered_ext = data[extension_field][data[extension_field] <= ext_max]
      begin = filtered_ext[filtered_stress >
                           sec_dev_thresh * filtered_stress.max()].min()

    # Determining the beginning point of the valid data based on a stress
    # threshold
    else:
      begin = data[extension_field][data[stress_field] >
                                    threshold * max_stress].min()

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame({identifier_field: [test_nr],
                               begin_field: [begin]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr], begin_field: [begin]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
