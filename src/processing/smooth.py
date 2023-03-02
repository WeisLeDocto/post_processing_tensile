# coding: utf-8

"""This script reads data from the source file, smoothens it using a
Savitzky-Golay filter except for the first column of data, and saves the
smoothened data at the provided location."""

import argparse
import pandas as pd
from scipy.signal import savgol_filter

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.get_nr import get_nr


if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Reads data from the source file, smoothens it using a "
                "Savitzky-Golay filter, and saves the smoothened data to the "
                "destination file.")
  parser.add_argument('source_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data to "
                           "smoothen.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where the smoothened data "
                           "should be saved.")
  parser.add_argument('nb_points', type=int, nargs=1,
                      help="The number of points to use for the Savitzky-Golay"
                           " filter smoothening the data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source = args.source_file[0]
  nb_points = args.nb_points[0]

  # Loading data from the source file
  test_nr = get_nr(source.parent)
  data = pd.read_csv(source)
  labels = data.keys()

  # Smoothening the data
  data[labels[1]] = savgol_filter(data[labels[1]], nb_points, 3)

  # Saving the values to the destination file
  data.to_csv(destination, index=False)
