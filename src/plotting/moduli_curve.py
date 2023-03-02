# coding: utf-8

"""This script reads the stress-strain data from a source file, as well as the
tangent moduli parameters from another file. It then plots the stress-strain
curve, along with the interpolation corresponding to the tangent moduli, and
saves the curve to the specified location."""

import argparse
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from ..tools.argparse_checkers import checker_is_tiff, checker_valid_csv
from ..tools.fields import identifier_field, \
  hyperelastic_offset_field as offset_field, \
  hyperelastic_modulus_field as hyper_field, \
  young_modulus_field as young_field, extension_field, stress_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Plots the stress-strain data contained in the source file "
                "into the destination file, and superimposes the lines "
                "corresponding to the Young's and hyperelastic modulus "
                "calculation.")
  parser.add_argument('destination_file', type=checker_is_tiff, nargs=1,
                      help="Path where the generated .tiff image should be "
                           "saved.")
  parser.add_argument('young_threshold', type=float, nargs=1,
                      help="The percentage of the total extension range over "
                           "which the Young's modulus was computed.")
  parser.add_argument('hyperelastic_threshold', type=float, nargs=1,
                      help="The percentage of the total extension range over "
                           "which the hyperelastic modulus was computed.")
  parser.add_argument('source_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the stress-strain"
                           " data to plot.")
  parser.add_argument('tangent_moduli_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the parameters of"
                           " the tangent moduli.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  source = args.source_file[0]
  destination = args.destination_file[0]
  moduli_file = args.tangent_moduli_file[0]
  young_threshold = args.young_threshold[0] / 100
  hyper_threshold = args.hyperelastic_threshold[0] / 100

  # Loading data from the source file
  test_nr = get_nr(source)
  data = pd.read_csv(source)

  # Reading data from the moduli file
  moduli = pd.read_csv(moduli_file)
  young = float(moduli[young_field][moduli[identifier_field] == test_nr])
  hyper = float(moduli[hyper_field][moduli[identifier_field] == test_nr])
  offset = float(moduli[offset_field][moduli[identifier_field] == test_nr])

  # Getting the extension range of the valid data
  min_extenso = data[extension_field].min()
  max_extenso = data[extension_field].max()
  extent = max_extenso - min_extenso

  # Generating the data for drawing the Young's modulus interpolation
  young_curve = (
    np.linspace(min_extenso, min_extenso + 3 * young_threshold * extent, 100),
    young * np.linspace(min_extenso - 1,
                        min_extenso + 3 * young_threshold * extent - 1, 100))
  # Generating the data for drawing the hyperelastic modulus interpolation
  hyper_curve = (
    np.linspace(max_extenso - 3 * hyper_threshold * extent, max_extenso, 100),
    offset + hyper * np.linspace(
      max_extenso - 3 * hyper_threshold * extent, max_extenso, 100))

  # Drawing the figure
  fig = plt.figure()
  ax = plt.subplot()
  # Drawing the stress-strain curve
  ax.plot(data[extension_field].values, data[stress_field].values)
  # Drawing the Young's and hyperelastic modulus interpolation
  ax.plot(young_curve[0], young_curve[1], '--k')
  ax.plot(hyper_curve[0], hyper_curve[1], '--r')
  # Setting the labels, legend, and saving the figure
  ax.set_xlabel(extension_field)
  ax.set_ylabel(stress_field)
  plt.legend(['Raw data', "Young's modulus", 'Hyperelastic modulus'])
  plt.savefig(destination, dpi=300)
