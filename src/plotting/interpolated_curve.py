# coding: utf-8

"""This script reads the stress-strain data from a source file, as well as Yeoh
parameters from another file. It then plots the stress-strain curve, along with
the stress predicted by Yeoh's model, and saves the curve to the specified
location."""

import argparse
from matplotlib import pyplot as plt
import pandas as pd

from ..tools.argparse_checkers import checker_is_tiff, checker_valid_csv
from ..tools.yeoh_model import yeoh_2
from ..tools.fields import identifier_field, yeoh_0_field, yeoh_1_field, \
  extension_field, stress_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Plots the stress-strain data contained in the source file "
                "into the destination file, and superimposes the stress "
                "predicted by Yeoh's model with the Yeoh parameters contained "
                "in the Yeoh file.")
  parser.add_argument('destination_file', type=checker_is_tiff, nargs=1,
                      help="Path where the generated .tiff image should be "
                           "saved.")
  parser.add_argument('source_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the stress-strain"
                           " data to plot.")
  parser.add_argument('yeoh_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the Yeoh "
                           "parameters.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  source = args.source_file[0]
  destination = args.destination_file[0]
  yeoh_file = args.yeoh_file[0]

  # Loading data from the source file
  test_nr = get_nr(source)
  data = pd.read_csv(source)

  # Reading data from the Yeoh parameter file
  yeoh = pd.read_csv(yeoh_file)
  c0 = float(yeoh[yeoh_0_field][yeoh[identifier_field] == test_nr])
  c1 = float(yeoh[yeoh_1_field][yeoh[identifier_field] == test_nr])

  # Calculating the stress with Yeoh's model
  fitted = yeoh_2(data[extension_field].values, c0, c1)

  # Drawing the figure
  fig = plt.figure()
  ax = plt.subplot()
  # Drawing the stress-strain data
  ax.plot(data[extension_field].values, data[stress_field].values)
  # Drawing the fitted curve
  ax.plot(data[extension_field].values, fitted, '--k')
  # Adding the axes labels, the legend, and saving the figure
  ax.set_xlabel(extension_field)
  ax.set_ylabel(stress_field)
  plt.legend(['Raw data', 'Fitted curve'])
  plt.savefig(destination, dpi=300)
