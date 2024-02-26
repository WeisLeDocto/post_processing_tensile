# This file contains the ranges over which to compute the tangent moduli

# The Young's modulus will be computed from the trimmed data between
# min_extension and min_extension + YOUNG_RANGE / 100 * (max_extension - min_extension)
export YOUNG_RANGE := 10
# The hyperelastic modulus will be computed from the trimmed data between
# max_extension - HYPERELASTIC_RANGE / 100 * (max_extension - min_extension) and max_extension
export HYPERELASTIC_RANGE := 5
