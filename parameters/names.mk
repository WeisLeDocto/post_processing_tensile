# This file contains all the variables holding the folder and file names

# Path to the experimental data files
TEST_DATA_FOLDER := test_data
NOTES_FILE := $(TEST_DATA_FOLDER)/notes.csv

# Names of the initial data files to read
EFFORT_FILE_NAME := effort.csv
POSITION_FILE_NAME := position.csv

# List of the valid effort data files
ALL_EFFORT_DATA := $(wildcard $(TEST_DATA_FOLDER)/*/$(EFFORT_FILE_NAME))
EFFORT_TO_EXCLUDE := $(TEST_DATA_FOLDER)/test_1/$(EFFORT_FILE_NAME) $(TEST_DATA_FOLDER)/test_2/$(EFFORT_FILE_NAME) $(TEST_DATA_FOLDER)/test_3/$(EFFORT_FILE_NAME)
VALID_EFFORT_DATA := $(filter-out $(EFFORT_TO_EXCLUDE), $(ALL_EFFORT_DATA))

# List of the valid position data files
ALL_POSITION_DATA := $(wildcard $(TEST_DATA_FOLDER)/*/$(POSITION_FILE_NAME))
POSITION_TO_EXCLUDE := $(TEST_DATA_FOLDER)/test_1/$(POSITION_FILE_NAME) $(TEST_DATA_FOLDER)/test_2/$(POSITION_FILE_NAME) $(TEST_DATA_FOLDER)/test_3/$(POSITION_FILE_NAME)
VALID_POSITION_DATA := $(filter-out $(POSITION_TO_EXCLUDE), $(ALL_POSITION_DATA))

# Path to the folders containing the data computed from the experimental data
COMPUTED_DATA_FOLDER := computed_data

# Paths to the smoothed data folder and files
SMOOTH_DATA_FOLDER := $(COMPUTED_DATA_FOLDER)/smooth
SMOOTH_EFFORT_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(SMOOTH_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(VALID_EFFORT_DATA))
SMOOTH_POSITION_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(POSITION_FILE_NAME), $(SMOOTH_DATA_FOLDER)/%/$(POSITION_FILE_NAME), $(VALID_POSITION_DATA))

# Paths to the stress-strain data folder and files
STRESS_STRAIN_DATA_FOLDER := $(COMPUTED_DATA_FOLDER)/stress_strain
STRESS_STRAIN_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(STRESS_STRAIN_DATA_FOLDER)/%.csv, $(VALID_EFFORT_DATA))
# Paths to the trimmed stress-strain data folder and files
TRIMMED_STRESS_STRAIN_DATA_FOLDER := $(COMPUTED_DATA_FOLDER)/trimmed_stress_strain
TRIMMED_STRESS_STRAIN_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(TRIMMED_STRESS_STRAIN_DATA_FOLDER)/%.csv, $(VALID_EFFORT_DATA))

# Paths to the data computed from the experimental data
RESULTS_FILE := results.csv
BEGIN_FILE := $(COMPUTED_DATA_FOLDER)/begin.csv
END_FILE := $(COMPUTED_DATA_FOLDER)/end.csv
YEOH_INTERPOLATION_FILE := $(COMPUTED_DATA_FOLDER)/yeoh_interpolation.csv
MAXIMUM_POINTS_FILE := $(COMPUTED_DATA_FOLDER)/max_point.csv
TANGENT_MODULI_FILE := $(COMPUTED_DATA_FOLDER)/tangent_moduli.csv

PYTHON_FOLDER := src

# Paths to the Python scripts to execute for processing data
SMOOTH_EXE_FILE := $(PYTHON_FOLDER)/processing/smooth.py
BEGIN_EXE_FILE := $(PYTHON_FOLDER)/processing/begin.py
END_EXE_FILE := $(PYTHON_FOLDER)/processing/end.py
TRIM_EXE_FILE := $(PYTHON_FOLDER)/processing/trim.py
STRESS_STRAIN_EXE_FILE := $(PYTHON_FOLDER)/processing/stress_strain.py
YEOH_EXE_FILE := $(PYTHON_FOLDER)/processing/yeoh.py
MAXIMUM_POINT_EXE_FILE := $(PYTHON_FOLDER)/processing/maximum_point.py
TANGENT_MODULI_EXE_FILE := $(PYTHON_FOLDER)/processing/tangent_moduli.py
RESULTS_EXE_FILE := $(PYTHON_FOLDER)/processing/results.py

# Executables for processing the data
SMOOTH_EXE := python -m $(PYTHON_FOLDER).processing.smooth
BEGIN_EXE := python -m $(PYTHON_FOLDER).processing.begin
END_EXE := python -m $(PYTHON_FOLDER).processing.end
TRIM_EXE := python -m $(PYTHON_FOLDER).processing.trim
STRESS_STRAIN_EXE := python -m $(PYTHON_FOLDER).processing.stress_strain
YEOH_EXE := python -m $(PYTHON_FOLDER).processing.yeoh
MAXIMUM_POINT_EXE := python -m $(PYTHON_FOLDER).processing.maximum_point
TANGENT_MODULI_EXE := python -m $(PYTHON_FOLDER).processing.tangent_moduli
RESULTS_EXE := python -m $(PYTHON_FOLDER).processing.results

# Paths to the Python scripts to execute for plotting data
SAVE_CURVE_EXE_FILE := $(PYTHON_FOLDER)/plotting/save_curve.py
BEGIN_END_CURVE_EXE_FILE := $(PYTHON_FOLDER)/plotting/begin_end_curve.py
ALL_STRESS_STRAIN_EXE_FILE := $(PYTHON_FOLDER)/plotting/all_stress_strain_curves.py
INTERPOLATED_CURVE_EXE_FILE := $(PYTHON_FOLDER)/plotting/interpolated_curve.py
TANGENT_MODULI_CURVE_EXE_FILE := $(PYTHON_FOLDER)/plotting/moduli_curve.py

# Paths to the Python scripts to execute for plotting data
SAVE_CURVE_EXE := python -m $(PYTHON_FOLDER).plotting.save_curve
BEGIN_END_CURVE_EXE := python -m $(PYTHON_FOLDER).plotting.begin_end_curve
ALL_STRESS_STRAIN_EXE := python -m $(PYTHON_FOLDER).plotting.all_stress_strain_curves
INTERPOLATED_CURVE_EXE := python -m $(PYTHON_FOLDER).plotting.interpolated_curve
TANGENT_MODULI_CURVE_EXE := python -m $(PYTHON_FOLDER).plotting.moduli_curve

# The folder containing all the plots
PLOTS_FOLDER := plots

# Paths to the raw plots folders and files
RAW_PLOTS_FOLDER := $(PLOTS_FOLDER)/raw_curves
RAW_PLOTS_EFFORT_FOLDER := $(RAW_PLOTS_FOLDER)/effort
RAW_PLOTS_POSITION_FOLDER := $(RAW_PLOTS_FOLDER)/position
RAW_PLOTS_EFFORT_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(RAW_PLOTS_EFFORT_FOLDER)/%.tiff, $(VALID_EFFORT_DATA))
RAW_PLOTS_POSITION_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(POSITION_FILE_NAME), $(RAW_PLOTS_POSITION_FOLDER)/%.tiff, $(VALID_POSITION_DATA))

# Paths to the smooth plots folders and files
SMOOTH_PLOTS_FOLDER := $(PLOTS_FOLDER)/smooth_curves
SMOOTH_PLOTS_EFFORT_FOLDER := $(SMOOTH_PLOTS_FOLDER)/effort
SMOOTH_PLOTS_POSITION_FOLDER := $(SMOOTH_PLOTS_FOLDER)/position
SMOOTH_PLOTS_EFFORT_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(SMOOTH_PLOTS_EFFORT_FOLDER)/%.tiff, $(VALID_EFFORT_DATA))
SMOOTH_PLOTS_POSITION_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(POSITION_FILE_NAME), $(SMOOTH_PLOTS_POSITION_FOLDER)/%.tiff, $(VALID_POSITION_DATA))

# Path to the begin and end plots folder and files
BEGIN_END_PLOTS_FOLDER := $(PLOTS_FOLDER)/begin_end_curves
BEGIN_END_PLOTS_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(BEGIN_END_PLOTS_FOLDER)/%.tiff, $(VALID_EFFORT_DATA))

# Paths to the stress-strain plots folder and files
STRESS_STRAIN_PLOTS_FOLDER := $(PLOTS_FOLDER)/stress_strain_curves
STRESS_STRAIN_PLOTS_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(STRESS_STRAIN_PLOTS_FOLDER)/%.tiff, $(VALID_EFFORT_DATA))
ALL_STRESS_STRAIN_CURVES := $(PLOTS_FOLDER)/all_stress_strain.tiff
ALL_STRESS_STRAIN_CURVES_TRIMMED := $(PLOTS_FOLDER)/all_stress_strain_trimmed.tiff

# Paths to the Yeoh interpolation plots folder and files
INTERPOLATION_CURVES_FOLDER := $(PLOTS_FOLDER)/yeoh_interpolated_curves
INTERPOLATION_PLOTS_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(INTERPOLATION_CURVES_FOLDER)/%.tiff, $(VALID_EFFORT_DATA))

# Paths to the tangent moduli plots folder and files
TANGENT_MODULI_CURVES_FOLDER := $(PLOTS_FOLDER)/tangent_moduli_curves
TANGENT_MODULI_PLOTS_FILES := $(patsubst $(TEST_DATA_FOLDER)/%/$(EFFORT_FILE_NAME), $(TANGENT_MODULI_CURVES_FOLDER)/%.tiff, $(VALID_EFFORT_DATA))