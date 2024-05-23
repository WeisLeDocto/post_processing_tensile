# The stress threshold used for detecting a local peak in the stress values
# will be PEAK_THRESHOLD / 100 * (max_stress - min_stress)
# The maximum width of the peak, as a number of samples, will be PEAK_RANGE
export PEAK_THRESHOLD := 1
export PEAK_RANGE := 10000
