# coding: utf-8

"""This script reads position and effort data from source files, as well as the
cross-sections and the initial length from the notes file. It then computes the
extension and the stress, and saves them at the provided location."""

import argparse
import numpy as np
import pandas as pd

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import (identifier_field, initial_length_field,
                            diameter_offset_field, diameter_field,
                            extension_field, stress_field,
                            time_field, position_field, effort_field)
from ..tools.get_nr import get_nr

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Reads the position and effort data from the source files, and"
                " metadata from the notes file. From these, the extension and "
                "the effort are computed and saved in the destination file.")
  parser.add_argument('source_position_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the position "
                           "data.")
  parser.add_argument('source_effort_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the effort "
                           "data.")
  parser.add_argument('notes_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the metadata "
                           "collected during the tests.")
  parser.add_argument('destination_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where to store the extension"
                           " and stress data.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  position_file = args.source_position_file[0]
  effort_file = args.source_effort_file[0]
  notes_file = args.notes_file[0]
  destination = args.destination_file[0]

  # Reading the data from the source files
  position = pd.read_csv(position_file)
  effort = pd.read_csv(effort_file)

  # Reading the metadata from the notes file
  test_nr = get_nr(destination)
  notes = pd.read_csv(notes_file)
  notes = notes[notes[identifier_field] == test_nr]

  # Calculating the extension from the position and the initial distance
  position['Total'] = position[position_field]
  position_interp = np.stack((effort[time_field].values,
                              np.interp(effort[time_field].values,
                                        position[time_field].values,
                                        position['Total'].values)), axis=1)
  init_length = float(notes[initial_length_field].iloc[0])
  position_interp[:, 1] += init_length - position_interp[0, 1]
  lambda_ = position_interp / [1, position_interp[0, 1]]

  # Getting the cross-section of the sample
  if diameter_offset_field is not None:
    section = np.pi * (notes[diameter_field].iloc[0] -
                       notes[diameter_offset_field].iloc[0]) ** 2 / 4
  else:
    section = np.pi * notes[diameter_field].iloc[0] ** 2 / 4

  # Calculating the stress from the effort and the section
  stress = effort[[time_field,
                   effort_field]].values / [1, section / 1e6]
  stress[:, 1] -= np.mean(stress[:200, 1])
  stress[:, 1] /= 1000

  # Saving the data to the destination file
  pd.DataFrame({extension_field: lambda_[:, 1],
                stress_field: stress[:, 1]}).to_csv(destination, index=False)
