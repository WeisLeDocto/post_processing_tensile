# This file contains all the variables holding the executable folder and file names

# Path to the Python interpreter to use
PYTHON_EXE := $(abspath venv/bin/python)

# Path to the source Python files for data processing
PYTHON_FOLDER := src/tensile_processing

# Name of the Python module to execute (must be installed for the given interpreter)
PYTHON_MODULE := tensile_processing

# Paths to the Python scripts to execute for processing data
SMOOTH_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/smooth.py)
BEGIN_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/begin.py)
END_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/end.py)
TRIM_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/trim.py)
STRESS_STRAIN_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/stress_strain.py)
YEOH_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/yeoh.py)
MAXIMUM_POINT_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/maximum_point.py)
TANGENT_MODULI_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/tangent_moduli.py)
RESULTS_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/results.py)

# Executables for processing the data
SMOOTH_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.smooth
BEGIN_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.begin
END_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.end
TRIM_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.trim
STRESS_STRAIN_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.stress_strain
YEOH_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.yeoh
MAXIMUM_POINT_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.maximum_point
TANGENT_MODULI_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.tangent_moduli
RESULTS_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.results

# Paths to the Python scripts to execute for plotting data
SAVE_CURVE_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/save_curve.py)
BEGIN_END_CURVE_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/begin_end_curve.py)
ALL_STRESS_STRAIN_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/all_stress_strain_curves.py)
INTERPOLATED_CURVE_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/interpolated_curve.py)
TANGENT_MODULI_CURVE_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/moduli_curve.py)

# Paths to the Python scripts to execute for plotting data
SAVE_CURVE_EXE := python -m $(PYTHON_MODULE).plotting.save_curve
BEGIN_END_CURVE_EXE := python -m $(PYTHON_MODULE).plotting.begin_end_curve
ALL_STRESS_STRAIN_EXE := python -m $(PYTHON_MODULE).plotting.all_stress_strain_curves
INTERPOLATED_CURVE_EXE := python -m $(PYTHON_MODULE).plotting.interpolated_curve
TANGENT_MODULI_CURVE_EXE := python -m $(PYTHON_MODULE).plotting.moduli_curve
