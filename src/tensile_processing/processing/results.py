# coding: utf-8

"""This script reads the data from all the generated .csv files, and combines
it into a single results file at the indicated location."""

import argparse
import pandas as pd

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv
from ..tools.fields import identifier_field

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Combines all the generated data into one single final results"
                " file.")
  parser.add_argument('notes_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the metadata from"
                           " the tests.")
  parser.add_argument('end_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data on the "
                           "end extensions.")
  parser.add_argument('begin_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data on the "
                           "begin extensions.")
  parser.add_argument('end_fit_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data on the "
                           "end extensions for a fit with Yeoh.")
  parser.add_argument('ultimate_strength_file', type=checker_valid_csv,
                      nargs=1, help="Path to the .csv file containing the "
                                    "ultimate strength data.")
  parser.add_argument('extensibility_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the "
                           "extensibility data.")
  parser.add_argument('yeoh_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data on the "
                           "Yeoh coefficients.")
  parser.add_argument('tangent_moduli_file', type=checker_valid_csv, nargs=1,
                      help="Path to the .csv file containing the data on the "
                           "tangent moduli.")
  parser.add_argument('results_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where all the data should be"
                           " aggregated.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  notes_file = args.notes_file[0]
  end_file = args.end_file[0]
  begin_file = args.begin_file[0]
  end_fit_file = args.end_fit_file[0]
  ultimate_strength_file = args.ultimate_strength_file[0]
  extensibility_file = args.extensibility_file[0]
  yeoh_file = args.yeoh_file[0]
  tangent_moduli_file = args.tangent_moduli_file[0]
  results_file = args.results_file[0]

  # Reading the data files
  notes = pd.read_csv(notes_file)
  end = pd.read_csv(end_file)
  begin = pd.read_csv(begin_file)
  end_fit = pd.read_csv(end_fit_file)
  ultimate_strength = pd.read_csv(ultimate_strength_file)
  extensibility = pd.read_csv(extensibility_file)
  yeoh = pd.read_csv(yeoh_file)
  moduli = pd.read_csv(tangent_moduli_file)

  # Aggregating the data into a single results file
  results = notes.copy(deep=True)
  results = results.join(end.set_index(identifier_field),
                         on=identifier_field)
  results = results.join(begin.set_index(identifier_field),
                         on=identifier_field)
  results = results.join(end_fit.set_index(identifier_field),
                         on=identifier_field)
  results = results.join(ultimate_strength.set_index(identifier_field),
                         on=identifier_field)
  results = results.join(extensibility.set_index(identifier_field),
                         on=identifier_field)
  results = results.join(yeoh.set_index(identifier_field),
                         on=identifier_field)
  results = results.join(moduli.set_index(identifier_field),
                         on=identifier_field)

  # Saving the results file at the requested destination
  results.to_csv(results_file, index=False)
