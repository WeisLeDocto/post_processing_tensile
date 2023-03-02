# coding: utf-8

"""This file contains the definition of the second-oder Yeoh model."""

import numpy as np


def yeoh_2(x: np.ndarray, c0: float, c1: float) -> np.ndarray:
  """Function implementing the second order Yeoh hyperelastic model.

  Args:
    x: The input array containing the extension data points.
    c0: The first Yeoh parameter.
    c1: The second Yeoh parameter.

  Returns:
    The array containing the stress data as predicted by the model.
  """

  return 2 * (x - 1 / x ** 2) * (c0 + 2 * c1 * (x ** 2 + 2 / x - 3))
