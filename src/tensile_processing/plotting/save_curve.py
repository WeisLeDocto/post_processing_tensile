# coding: utf-8

"""This script reads data from a source file, and plots each column of data
against the first column. The generated figure is then saved to the specified
location."""

import argparse
from matplotlib import pyplot as plt
import pandas as pd

from ..tools import checker_is_tiff, checker_valid_csv


if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Plots the data contained in the source file into the "
                "destination file. The data of each columns is plotted against"
                "that of the first column.")
  parser.add_argument('source_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data to "
                           "plot.")
  parser.add_argument('destination_file', type=checker_is_tiff, nargs=1,
                      help="Path where the generated .tiff image should be "
                           "saved.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  source = args.source_file[0]
  destination = args.destination_file[0]

  # Loading data from the source file
  data = pd.read_csv(source)

  # Drawing the figure
  fig = plt.figure()
  # Plotting each column from the source file
  for i in range(1, data.shape[1]):
    ax = plt.subplot(data.shape[1] - 1, 1, i)
    ax.plot(data.iloc[:, 0], data.iloc[:, i])
    ax.set_xlabel(data.keys()[0])
    ax.set_ylabel(data.keys()[i])
  # Saving the figure
  plt.savefig(destination, dpi=300)
