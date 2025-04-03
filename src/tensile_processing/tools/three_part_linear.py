# coding: utf-8

import numpy as np


def three_part_linear(x0: float,
                      x3: float,
                      x: np.ndarray,
                      y0: float,
                      x1: float,
                      y1: float,
                      x2: float,
                      y2: float,
                      y3: float) -> np.ndarray:
  """"""

  p0 = y0 + (y1 - y0) / (x1 - x0) * (x - x0)
  p0_mask = x < x1

  p2 = y2 + (y3 - y2) / (x3 - x2) * (x - x2)
  p2_mask = x > x2

  p1 = y1 + (y2 - y1) / (x2 - x1) * (x - x1)
  p1_mask = ~(p0_mask | p2_mask)

  return p0_mask * p0 + p1_mask * p1 + p2_mask * p2
