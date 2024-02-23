# coding: utf-8

"""This script reads the stress-strain data from source files, then computes
the Yeoh coefficients, and saves the coefficients at the provided location."""

import argparse
import pandas as pd
from scipy.optimize import curve_fit
from typing import Optional

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.yeoh_model import yeoh_2
from ..tools.fields import identifier_field, yeoh_0_field, yeoh_1_field, \
  extension_field, stress_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':
  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="For each source file determines the Yeoh coefficients from "
                "the stress-strain data, and then stores the coefficients in "
                "the destination file.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to store the Yeoh "
                           "coefficients.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source_files = args.source_files

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)
  # Creating the dataframe to save
  to_write: Optional[pd.DataFrame] = None

  # Iterating over the source files
  for path in source_files:
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)

    # Fitting the Yeoh coefficients to the experimental data
    fit, *_ = curve_fit(yeoh_2, data[extension_field].values,
                        data[stress_field].values)

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame({identifier_field: [test_nr],
                               yeoh_0_field: [fit[0]],
                               yeoh_1_field: [fit[1]]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr],
         yeoh_0_field: [fit[0]],
         yeoh_1_field: [fit[1]]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
