# coding: utf-8

"""This script reads the stress-strain data from source files, then computes
the Young and hyperelastic modulus, and saves the moduli coefficients at the
provided location."""

import argparse
import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import Polynomial
from typing import Optional

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import identifier_field, young_modulus_field, \
  hyperelastic_offset_field, hyperelastic_modulus_field, extension_field, \
  stress_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="For each source file determines the Young and hyperelastic "
                "modulus from the stress-strain data, and then stores the "
                "moduli coefficients in the destination file.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to store the tangent "
                           "moduli coefficients.")
  parser.add_argument('young_threshold', type=float, nargs=1,
                      help="The percentage of the total extension range over "
                           "which the Young's modulus should be computed.")
  parser.add_argument('hyperelastic_threshold', type=float, nargs=1,
                      help="The percentage of the total extension range over "
                           "which the hyperelastic modulus should be "
                           "computed.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help="Paths to the .csv files containing the "
                           "stress-strain data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source_files = args.source_files
  young_threshold = args.young_threshold[0] / 100
  hyper_threshold = args.hyperelastic_threshold[0] / 100

  # Sorting the source files according to the test number
  source_files = sorted(source_files, key=get_nr)
  # Creating the dataframe to save
  to_write: Optional[pd.DataFrame] = None

  # Iterating over the source files
  for path in source_files:
    # Reading data from the source file
    test_nr = get_nr(path)
    data = pd.read_csv(path)

    # Getting subsets of the data for each modulus
    min_extenso = data[extension_field].min()
    max_extenso = data[extension_field].max()
    extent = max_extenso - min_extenso
    data_young = data[data[extension_field] <= min_extenso
                      + young_threshold * extent]
    data_hyper = data[data[extension_field] >= max_extenso -
                      hyper_threshold * extent]

    # Calculating the Young's modulus
    young, *_ = np.linalg.lstsq(
      (data_young[extension_field].values - 1)[:, np.newaxis],
      data_young[stress_field].values[:, np.newaxis], rcond=None)
    young = float(np.squeeze(young))

    # Calculating the hyperelastic modulus
    hyperelastic_fit = Polynomial.fit(data_hyper[extension_field].values,
                                      data_hyper[stress_field].values, 1)
    hyperelastic = hyperelastic_fit.convert().coef[1]
    offset = hyperelastic_fit.convert().coef[0]

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = pd.DataFrame(
        {identifier_field: [test_nr], young_modulus_field: [young],
         hyperelastic_offset_field: [offset],
         hyperelastic_modulus_field: [hyperelastic]})
    else:
      to_write = pd.concat((to_write, pd.DataFrame(
        {identifier_field: [test_nr], young_modulus_field: [young],
         hyperelastic_offset_field: [offset],
         hyperelastic_modulus_field: [hyperelastic]})))

  # Saving the values to the destination file
  to_write.to_csv(destination, index=False)
