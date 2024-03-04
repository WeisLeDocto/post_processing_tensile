# coding: utf-8

"""This script reads the data from all the generated results .csv files when
running the Make command over an entire directory, and combines it into a
single global results file at the indicated location."""

import argparse
import pandas as pd
from typing import Optional
from re import search

from ..tools.argparse_checkers import checker_is_csv, checker_valid_csv

if __name__ == '__main__':

  # Parser for parsing the command line arguments of the script
  parser = argparse.ArgumentParser(
    description="Combines all the generated results data into one single "
                "global results file.")
  parser.add_argument('source_results_files', type=checker_valid_csv,
                      nargs='+', help="Paths to the .csv files containing the "
                                      "results data.")
  parser.add_argument('global_results_file', type=checker_is_csv, nargs=1,
                      help="Path to the .csv file where all the data should be"
                           " aggregated.")
  args = parser.parse_args()

  # Getting the arguments from the parser
  source_results_files = args.source_results_files
  global_results_file = args.global_results_file[0]

  to_write: Optional[pd.DataFrame] = None

  for path in source_results_files:

    # Reading data from the source file
    data = pd.read_csv(path)

    # Adding the donor and time point information to the existing data
    data['Donor'], *_ = search(r"(\w+)_", path.parent.parent.name).groups()
    data['Timepoint'] = path.parent.name

    # Rearranging the columns to have the donor and time point first
    labels = data.columns.tolist()
    labels.remove('Donor')
    labels.remove('Timepoint')
    labels.insert(0, 'Timepoint')
    labels.insert(0, 'Donor')
    data = data[labels]

    # Adding the values to the dataframe to save
    if to_write is None:
      to_write = data.copy()
    else:
      to_write = pd.concat((to_write, data), ignore_index=True)

  # Saving the values to the destination file
  to_write.to_csv(global_results_file, index=False)
