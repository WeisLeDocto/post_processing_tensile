# coding: utf-8

"""This script reads the stress-strain data from the specified files and draws
it all on a single graph. It labels the curves according to their category as
read from the notes file."""

import argparse
from matplotlib import pyplot as plt
import pandas as pd

from ..tools.argparse_checkers import checker_is_tiff, checker_valid_csv
from ..tools.fields import identifier_field, type_field, condition_field, \
  extension_field, stress_field
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Plots all the stress-strain curves from the source files into"
                " a single destination file, with labels extracted from the "
                "notes file.")
  parser.add_argument('notes_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the metadata "
                           "related to the tests.")
  parser.add_argument('destination_file', type=checker_is_tiff, nargs=1,
                      help="Path where the generated .tiff image should be "
                           "saved.")
  parser.add_argument('source_files', type=checker_valid_csv, nargs='+',
                      help='Paths to the .csv files containing the data to '
                           'plot.')
  args = parser.parse_args()

  # Getting the arguments from the parser
  notes_file = args.notes_file[0]
  destination = args.destination_file[0]
  source_files = args.source_files

  # Extracting the metadata
  notes = pd.read_csv(notes_file)

  # Creating the figure to plot the curves on
  fig = plt.figure()
  ax = plt.subplot()
  prop_cycle = plt.rcParams['axes.prop_cycle']
  colors = iter(prop_cycle.by_key()['color'])

  color_by_label = dict()
  for path in source_files:
    # Extracting the data from the file
    data = pd.read_csv(path)
    test_nr = get_nr(path)
    # Extracting data from the notes file
    condition = notes[condition_field][notes[identifier_field] == test_nr]
    type_ = notes[type_field][notes[identifier_field] == test_nr]

    # Getting the label associated to the file
    label = f'{type_.values[0]} {condition.values[0]}'
    # Getting the color for the current curve
    if label not in color_by_label:
      color = next(colors)
      color_by_label[label] = color
    else:
      color = color_by_label[label]

    # Plotting the data
    ax.plot(data[extension_field].values, data[stress_field].values,
            label=label, color=color)

  # Setting the axes labels and the title
  ax.set_title('All stress-strain curves')
  ax.set_xlabel(extension_field)
  ax.set_ylabel(stress_field)

  # Ensuring the labels are unique
  handles, labels = plt.gca().get_legend_handles_labels()
  by_label = dict(zip(labels, handles))
  plt.legend(by_label.values(), by_label.keys())

  # Saving the figure
  plt.savefig(destination, dpi=300)
