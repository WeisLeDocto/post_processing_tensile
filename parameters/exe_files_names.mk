# This file contains all the variables holding the executable folder and file names

# Path to the Python interpreter to use
export PYTHON_EXE := $(abspath venv/bin/python)

# Path to the source Python files for data processing
export PYTHON_FOLDER := src/tensile_processing

# Name of the Python module to execute (must be installed for the given interpreter)
export PYTHON_MODULE := tensile_processing

# Paths to the Python scripts to execute for processing data
export SMOOTH_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/smooth.py)
export BEGIN_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/begin.py)
export END_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/end.py)
export TRIM_BEGIN_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/trim_begin.py)
export TRIM_END_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/trim_end.py)
export STRESS_STRAIN_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/stress_strain.py)
export YEOH_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/yeoh.py)
export ULTIMATE_STRENGTH_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/ultimate_strength.py)
export EXTENSIBILITY_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/extensibility.py)
export TANGENT_MODULI_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/tangent_moduli.py)
export RESULTS_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/results.py)
# Doesn't need to be exported as it is only run by the top-level Makefile
GLOBAL_RESULTS_EXE_FILE := $(abspath $(PYTHON_FOLDER)/processing/global_results.py)

# Executables for processing the data
export SMOOTH_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.smooth
export BEGIN_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.begin
export END_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.end
export TRIM_BEGIN_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.trim_begin
export TRIM_END_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.trim_end
export STRESS_STRAIN_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.stress_strain
export YEOH_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.yeoh
export ULTIMATE_STRENGTH_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.ultimate_strength
export EXTENSIBILITY_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.extensibility
export TANGENT_MODULI_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.tangent_moduli
export RESULTS_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.results
# Doesn't need to be exported as it is only run by the top-level Makefile
GLOBAL_RESULTS_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).processing.global_results

# Paths to the Python scripts to execute for plotting data
export SAVE_CURVE_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/save_curve.py)
export BEGIN_END_CURVE_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/begin_end_curve.py)
export ALL_STRESS_STRAIN_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/all_stress_strain_curves.py)
export INTERPOLATED_CURVE_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/interpolated_curve.py)
export TANGENT_MODULI_CURVE_EXE_FILE := $(abspath $(PYTHON_FOLDER)/plotting/moduli_curve.py)

# Paths to the Python scripts to execute for plotting data
export SAVE_CURVE_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).plotting.save_curve
export BEGIN_END_CURVE_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).plotting.begin_end_curve
export ALL_STRESS_STRAIN_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).plotting.all_stress_strain_curves
export INTERPOLATED_CURVE_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).plotting.interpolated_curve
export TANGENT_MODULI_CURVE_EXE := $(PYTHON_EXE) -m $(PYTHON_MODULE).plotting.moduli_curve
