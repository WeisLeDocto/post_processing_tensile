# This file contains the recipes for computing the results from the experimental data
# of monotonic uni-axial tensile tests

# Paths to the .mk files containing the parameters to use for processing the data
PARAMETERS_FOLDER := parameters
NAMES_FILE := $(PARAMETERS_FOLDER)/names.mk
NUMBER_POINTS_SMOOTH_FILE := $(PARAMETERS_FOLDER)/nb_pts_smooth.mk
NUMBER_POINTS_BEGIN_END_FILE := $(PARAMETERS_FOLDER)/nb_pts_begin_end.mk
STRESS_THRESHOLD_FILE := $(PARAMETERS_FOLDER)/stress_thresh.mk
MODULI_RANGES_FILE := $(PARAMETERS_FOLDER)/moduli_ranges.mk

# Including the .mk files
include $(NAMES_FILE)
include $(NUMBER_POINTS_SMOOTH_FILE)
include $(NUMBER_POINTS_BEGIN_END_FILE)
include $(STRESS_THRESHOLD_FILE)
include $(MODULI_RANGES_FILE)

.PHONY : help
help: ## Displays this help documentation
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: results plots ## Computes the results and plots the data

.PHONY: results
results: $(RESULTS_FILE) ## Assembles all the intermediate .csv results files into one final .csv result file

.PHONY: plots
plots: raw_plots smooth_plots begin_end_plots stress_strain_plots yeoh_interpolation_plots tangent_moduli_plots ## Plots curves from the intermediate data files to visualize the data

.PHONY: clean
clean: ## Deletes all the results and plots files
	@rm -rf $(COMPUTED_DATA_FOLDER) $(PLOTS_FOLDER) $(RESULTS_FILE)

.PHONY: smooth
smooth: $(SMOOTH_EFFORT_FILES) $(SMOOTH_POSITION_FILES) ## Smoothens the raw data and saves the smoothed data to a .csv file

# Smoothens the raw effort data and saves the smoothed data to a .csv file for each test
$(SMOOTH_DATA_FOLDER)/%/$(EFFORT_FILE_NAME): $(SMOOTH_EXE_FILE) $(NUMBER_POINTS_SMOOTH_FILE) $(addprefix $(TEST_DATA_FOLDER)/, %/$(EFFORT_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(SMOOTH_EXE) $(abspath $(filter-out $< $(NUMBER_POINTS_SMOOTH_FILE), $^)) $(abspath $@) $(NB_POINTS_SMOOTH)

# Simply copies the position data to the smoothed data folder, as the position data is already smooth
$(SMOOTH_DATA_FOLDER)/%/$(POSITION_FILE_NAME): $(addprefix $(TEST_DATA_FOLDER)/, %/$(POSITION_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Writing $@"
	@cp $< $@

.PHONY: stress_strain
stress_strain: $(STRESS_STRAIN_FILES) ## Computes the stress and the strain from the position and effort files, and saves them to a .csv file for each test

$(STRESS_STRAIN_DATA_FOLDER)/%.csv: $(STRESS_STRAIN_EXE_FILE) $(addprefix $(SMOOTH_DATA_FOLDER)/, %/$(POSITION_FILE_NAME)) $(addprefix $(SMOOTH_DATA_FOLDER)/, %/$(EFFORT_FILE_NAME)) $(NOTES_FILE)
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(STRESS_STRAIN_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

.PHONY: max_points
max_points: $(MAXIMUM_POINTS_FILE) ## Detects the ultimate strength and the extensibility from the stress-strain data for each test, and saves the values to a .csv file

$(MAXIMUM_POINTS_FILE): $(MAXIMUM_POINT_EXE_FILE) $(STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(MAXIMUM_POINT_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: begin
begin: $(BEGIN_FILE) ## Detects the begin extension of the valid stress-strain data for each test, and saves it to a .csv file

$(BEGIN_FILE): $(BEGIN_EXE_FILE) $(MAXIMUM_POINTS_FILE) $(STRESS_STRAIN_FILES) $(STRESS_THRESHOLD_FILE)
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(BEGIN_EXE) $(abspath $@) $(STRESS_THRESHOLD) $(abspath $(filter-out $< $(STRESS_THRESHOLD_FILE), $^))

.PHONY: end
end: $(END_FILE) ## Detects the end extension of the valid stress-strain data for each test, and saves it to a .csv file

$(END_FILE): $(END_EXE_FILE) $(BEGIN_FILE) $(NUMBER_POINTS_BEGIN_END_FILE) $(STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(END_EXE) $(abspath $@) $(NB_POINTS_SMOOTH_END) $(abspath $(filter-out $< $(NUMBER_POINTS_BEGIN_END_FILE), $^))

.PHONY: trim
trim: $(TRIMMED_STRESS_STRAIN_FILES) ## Takes the stress-strain data as an input, and saves only the valid part of it to a .csv file for each test

$(TRIMMED_STRESS_STRAIN_DATA_FOLDER)/%.csv: $(TRIM_EXE_FILE) $(STRESS_STRAIN_DATA_FOLDER)/%.csv $(BEGIN_FILE) $(END_FILE)
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(TRIM_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: yeoh_interpolation
yeoh_interpolation: $(YEOH_INTERPOLATION_FILE) ## Fits a second-order Yeoh model to the valid stress-strain data for each test, and saves the parameters to a .csv file

$(YEOH_INTERPOLATION_FILE): $(YEOH_EXE_FILE) $(TRIMMED_STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(YEOH_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: tangent_moduli
tangent_moduli: $(TANGENT_MODULI_FILE) ## Calculates the tangent moduli at both ends of the valid stress-strain data for each test, and saves the slopes to a .csv file

$(TANGENT_MODULI_FILE): $(TANGENT_MODULI_EXE_FILE) $(MODULI_RANGES_FILE) $(TRIMMED_STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(TANGENT_MODULI_EXE) $(abspath $@) $(YOUNG_RANGE) $(HYPERELASTIC_RANGE) $(abspath $(filter-out $< $(MODULI_RANGES_FILE), $^))

$(RESULTS_FILE): $(RESULTS_EXE_FILE) $(NOTES_FILE) $(BEGIN_FILE) $(END_FILE) $(MAXIMUM_POINTS_FILE) $(YEOH_INTERPOLATION_FILE) $(TANGENT_MODULI_FILE)
	@mkdir -p $(@D)
	@echo "Writing $@"
	@$(RESULTS_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

.PHONY: raw_plots
raw_plots: $(RAW_PLOTS_EFFORT_FILES) $(RAW_PLOTS_POSITION_FILES) ## Plots the raw data points in .tiff files for each test

$(RAW_PLOTS_EFFORT_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(addprefix $(TEST_DATA_FOLDER)/, %/$(EFFORT_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

$(RAW_PLOTS_POSITION_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(addprefix $(TEST_DATA_FOLDER)/, %/$(POSITION_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

.PHONY: smooth_plots
smooth_plots: $(SMOOTH_PLOTS_EFFORT_FILES) $(SMOOTH_PLOTS_POSITION_FILES) ## Plots the smoothed data points in .tiff files for each test

$(SMOOTH_PLOTS_EFFORT_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(addprefix $(SMOOTH_DATA_FOLDER)/, %/$(EFFORT_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

$(SMOOTH_PLOTS_POSITION_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(addprefix $(SMOOTH_DATA_FOLDER)/, %/$(POSITION_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

.PHONY: begin_end_plots
begin_end_plots: $(BEGIN_END_PLOTS_FILES) ## Plots the stress_strain data in .tiff files for each test, with vertical lines indicating the begin and end cutoff extension

$(BEGIN_END_PLOTS_FOLDER)/%.tiff: $(BEGIN_END_CURVE_EXE_FILE) $(STRESS_STRAIN_DATA_FOLDER)/%.csv $(BEGIN_FILE) $(END_FILE)
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(BEGIN_END_CURVE_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: stress_strain_plots
stress_strain_plots: $(STRESS_STRAIN_PLOTS_FILES) $(ALL_STRESS_STRAIN_CURVES) $(ALL_STRESS_STRAIN_CURVES_TRIMMED) ## Plots the stress-strain data in .tiff files for each test, as well a one .tiff file of all the stress-strain data and one .tiff file of all the trimmed stress-strain data

$(STRESS_STRAIN_PLOTS_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(STRESS_STRAIN_DATA_FOLDER)/%.csv
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

$(ALL_STRESS_STRAIN_CURVES): $(ALL_STRESS_STRAIN_EXE_FILE) $(NOTES_FILE) $(STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(ALL_STRESS_STRAIN_EXE) $(abspath $(word 2,$^)) $(abspath $@) $(abspath $(filter-out $< $(NOTES_FILE), $^))

$(ALL_STRESS_STRAIN_CURVES_TRIMMED): $(ALL_STRESS_STRAIN_EXE_FILE) $(NOTES_FILE) $(TRIMMED_STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(ALL_STRESS_STRAIN_EXE) $(abspath $(word 2,$^)) $(abspath $@) $(abspath $(filter-out $< $(NOTES_FILE), $^))

.PHONY: yeoh_interpolation_plots
yeoh_interpolation_plots: $(INTERPOLATION_PLOTS_FILES) ## Plots the valid stress-strain data in a .tiff file for each test, with the fit of the Yeoh model superimposed

$(INTERPOLATION_CURVES_FOLDER)/%.tiff: $(INTERPOLATED_CURVE_EXE_FILE) $(TRIMMED_STRESS_STRAIN_DATA_FOLDER)/%.csv $(YEOH_INTERPOLATION_FILE)
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(INTERPOLATED_CURVE_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: tangent_moduli_plots
tangent_moduli_plots: $(TANGENT_MODULI_PLOTS_FILES) ## Plots the valid stress-strain data in a .tiff file for each test, with the fit of the tangent moduli superimposed

$(TANGENT_MODULI_CURVES_FOLDER)/%.tiff: $(TANGENT_MODULI_CURVE_EXE_FILE) $(MODULI_RANGES_FILE) $(TRIMMED_STRESS_STRAIN_DATA_FOLDER)/%.csv $(TANGENT_MODULI_FILE)
	@mkdir -p $(@D)
	@echo "Plotting $@"
	@$(TANGENT_MODULI_CURVE_EXE) $(abspath $@) $(YOUNG_RANGE) $(HYPERELASTIC_RANGE) $(abspath $(filter-out $< $(MODULI_RANGES_FILE), $^))
