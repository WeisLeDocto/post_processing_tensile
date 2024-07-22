# If true, the second derivative method is used for determining the end
# extension of the valid data. Otherwise, the maximum of the first derivative
# is used.
export USE_SECOND_DERIVATIVE_END := true

# The number of points to use for the Savitzky–Golay filter applied when
# determining the end extension of the valid data
export NB_POINTS_SMOOTH_END := 2000
