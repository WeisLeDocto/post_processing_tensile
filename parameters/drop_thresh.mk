# The stress threshold used for detecting a sudden drop in the stress values
# will be DROP_THRESHOLD / 100 * (max_stress - min_stress)
# The search will be performed over DROP_RANGE consecutive data points
DROP_THRESHOLD := 1
DROP_RANGE := 1000
