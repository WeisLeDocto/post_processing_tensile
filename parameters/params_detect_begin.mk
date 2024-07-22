# If true, the second derivative method is used for determining the begin
# extension of the valid data. Otherwise, the stress threshold method is used.
export USE_SECOND_DERIVATIVE_BEGIN := true

# The stress threshold used for determining the begin extension of the valid
# data will be BEGIN_STRESS_THRESHOLD / 100 * (max_stress - min_stress), if
# using the stress threshold method
export BEGIN_STRESS_THRESHOLD := 2

# The number of points to use for the Savitzky–Golay filter applied when
# determining the begin extension of the valid data, if using the second
# derivative method
export NB_POINTS_SMOOTH_BEGIN := 2000
# The second derivative threshold used for determining the begin extension of
# the valid data will be
# SECOND_DERIVATIVE_THRESHOLD / 100 * max_second_derivative, if
# using the second derivative method
export SECOND_DERIVATIVE_THRESHOLD := 15
