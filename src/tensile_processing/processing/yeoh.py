# coding: utf-8

"""This script reads the stress-strain data from source files, then computes
the Yeoh coefficients, and saves the coefficients at the provided location."""

import argparse
import pandas as pd
from scipy.optimize import curve_fit
from typing import Optional
from functools import partial

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.three_part_linear import three_part_linear
from ..tools.fields import (identifier_field, x0_field, y0_field, x1_field,
                            y1_field, x2_field, y2_field, x3_field, y3_field,
                            extension_field, stress_field)
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
    p0 = (data[stress_field].min(),
          0.5, data[stress_field].min(),
          1.0, data[stress_field].max() / 10,
          data[stress_field].max())
    amp = data[stress_field].max() - data[stress_field].min()
    low_bound = data[stress_field].min() - 0.2 * amp
    high_bound = data[stress_field].max() + 0.2 * amp
    bounds_min = (low_bound,
                  0.4, low_bound,
                  0.8, low_bound,
                  low_bound)
    bounds_max = (high_bound,
                  0.6, high_bound,
                  1.2, high_bound,
                  high_bound)

    fit, *_ = curve_fit(partial(three_part_linear,
                                data[extension_field].min(),
                                data[extension_field].max()),
                        data[extension_field].values,
                        data[stress_field].values, p0=p0,
                        bounds=(bounds_min, bounds_max))

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame({identifier_field: [test_nr],
                               x0_field: [data[extension_field].min()],
                               y0_field: [fit[0]],
                               x1_field: [fit[1]],
                               y1_field: [fit[2]],
                               x2_field: [fit[3]],
                               y2_field: [fit[4]],
                               x3_field: [data[extension_field].max()],
                               y3_field: [fit[5]]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr],
         x0_field: [data[extension_field].min()],
         y0_field: [fit[0]],
         x1_field: [fit[1]],
         y1_field: [fit[2]],
         x2_field: [fit[3]],
         y2_field: [fit[4]],
         x3_field: [data[extension_field].max()],
         y3_field: [fit[5]]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
