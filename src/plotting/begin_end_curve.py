# coding: utf-8

"""This script reads the stress-strain data from a source file, as well as the
beginning and end extension cutoffs from other files. It then plots the
stress-strain curve, along with vertical lines indicating the beginning and end
cutoffs, and saves the curve to the specified location."""

import argparse
from matplotlib import pyplot as plt
import pandas as pd

from ..tools.argparse_checkers import checker_is_tiff, checker_valid_csv
from ..tools.fields import identifier_field, begin_field, end_field, \
  extension_field, stress_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Plots the stress-strain data contained in the source file "
                "into the destination file, and highlights the valid data as "
                "defined in the begin and end files.")
  parser.add_argument('destination_file', type=checker_is_tiff, nargs=1,
                      help="Path where the generated .tiff image should be "
                           "saved.")
  parser.add_argument('source_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the stress-strain"
                           " data to plot.")
  parser.add_argument('begin_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the minimum "
                           "extension of the valid data.")
  parser.add_argument('end_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the maximum "
                           "extension of the valid data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  destination = args.destination_file[0]
  source = args.source_file[0]
  begin_file = args.begin_file[0]
  end_file = args.end_file[0]

  # Extracting data from the source file
  test_nr = get_nr(source)
  data = pd.read_csv(source)

  # Extracting the beginning and end timestamps
  begins = pd.read_csv(begin_file)
  begin = float(begins[begin_field]
                [begins[identifier_field] == test_nr].iloc[0])
  ends = pd.read_csv(end_file)
  end = float(ends[end_field][ends[identifier_field] == test_nr].iloc[0])

  # Dividing data into three categories
  before = data[data[extension_field] < begin]
  after = data[data[extension_field] > end]
  valid = data[(data[extension_field] >= begin) &
               (data[extension_field] <= end)]

  # Drawing the figure
  fig = plt.figure()
  ax = plt.subplot()
  # Drawing the valid data
  ax.plot(valid[extension_field], valid[stress_field])
  ax.axvline(x=begin, color='k')
  # Drawing the data before the begin cutoff
  ax.plot(before[extension_field].values, before[stress_field].values,
          color='#888888')
  ax.axvline(x=end, color='k')
  # Drawing the data after the end cutoff
  ax.plot(after[extension_field], after[stress_field], color='#888888')
  # Setting the axes labels and saving the figure
  ax.set_xlabel(extension_field)
  ax.set_ylabel(stress_field)
  plt.savefig(destination, dpi=300)
