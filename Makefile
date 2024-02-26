# This file contains the recipes for computing the results from the experimental data
# of monotonic uni-axial tensile tests

# Paths to the .mk files containing the parameters to use for processing the data
PARAMETERS_FOLDER := parameters
DATA_NAMES_FILE := $(abspath $(PARAMETERS_FOLDER)/data_files_names.mk)
# The following names are only defined by the parent of level 0, never by the children
# They are exported for the children to include
ifeq ($(MAKELEVEL),0)
	export EXE_NAMES_FILE := $(abspath $(PARAMETERS_FOLDER)/exe_files_names.mk)
	export NUMBER_POINTS_SMOOTH_FILE := $(abspath $(PARAMETERS_FOLDER)/nb_pts_smooth.mk)
	export NUMBER_POINTS_BEGIN_END_FILE := $(abspath $(PARAMETERS_FOLDER)/nb_pts_smooth_end.mk)
	export STRESS_THRESHOLD_FILE := $(abspath $(PARAMETERS_FOLDER)/stress_thresh.mk)
	export MODULI_RANGES_FILE := $(abspath $(PARAMETERS_FOLDER)/moduli_ranges.mk)
	export DROP_THRESHOLD_FILE := $(abspath $(PARAMETERS_FOLDER)/drop_thresh.mk)
endif

# Including the .mk files
include $(DATA_NAMES_FILE)
# The following ones are imported from parent if MAKELEVEL is not 0
ifeq ($(MAKELEVEL),0)
	include $(EXE_NAMES_FILE)
	include $(NUMBER_POINTS_SMOOTH_FILE)
	include $(NUMBER_POINTS_BEGIN_END_FILE)
	include $(STRESS_THRESHOLD_FILE)
	include $(MODULI_RANGES_FILE)
	include $(DROP_THRESHOLD_FILE)
endif

# Calling Makefiles recursively in the target directory only if the TARGET_DIRECTORY variable is set by the user
# Otherwise, applying the recipes to the current directory
ifeq ($(MAKELEVEL),0)
	ifdef TARGET_DIRECTORY
		RECURSIVE := true
		DATA_DIRECTORIES := $(dir $(abspath $(wildcard $(TARGET_DIRECTORY)*/*/Makefile)))
	else
		RECURSIVE := false
		DATA_DIRECTORIES := ./
	endif
else
	RECURSIVE := false
	DATA_DIRECTORIES := ./
endif

# The first three recipes are common to the RECURSIVE and non-RECURSIVE usage modes
.PHONY : help
help: ## Displays this help documentation
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: results plots ## Computes the results and plots the data

.PHONY: plots
plots: raw_plots smooth_plots begin_end_plots stress_strain_plots yeoh_interpolation_plots tangent_moduli_plots ## Plots curves from the intermediate data files to visualize the data

ifeq ($(RECURSIVE),true)
# Recipes used when running this Makefile at top level and specifying a TARGET_DIRECTORY variable
# No local results are computed, only calls to sub-Makefiles are issued

# Smart way to call the targets in the sub-Makefiles without explicitly naling them
$(DATA_DIRECTORIES)::
	@$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: results clean smooth stress_strain max_points begin end trim tangent_moduli raw_plots smooth_plots begin_end_plots stress_strain_plots yeoh_interpolation_plots tangent_moduli_plots
results clean smooth stress_strain max_points begin end trim tangent_moduli raw_plots smooth_plots begin_end_plots stress_strain_plots yeoh_interpolation_plots tangent_moduli_plots: $(DATA_DIRECTORIES)

else
# Recipes used when running this Makefile at top level without specifying a TARGET_DIRECTORY variable, or running it as a sub-Makefile
# Only local results are computed, no sub-Makefile is ever called

.PHONY: results
results: $(RESULTS_FILE) ## Assembles all the intermediate .csv results files into one final .csv result file

.PHONY: clean
clean: ## Deletes all the results and plots files
	@rm -rf $(COMPUTED_DATA_FOLDER) $(PLOTS_FOLDER) $(RESULTS_FILE)

.PHONY: smooth
smooth: $(SMOOTH_EFFORT_FILES) $(SMOOTH_POSITION_FILES) ## Smoothens the raw data and saves the smoothed data to a .csv file

# Smoothens the raw effort data and saves the smoothed data to a .csv file for each test
$(SMOOTH_DATA_FOLDER)/%/$(EFFORT_FILE_NAME): $(SMOOTH_EXE_FILE) $(NUMBER_POINTS_SMOOTH_FILE) $(addprefix $(TEST_DATA_FOLDER)/, %/$(EFFORT_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(SMOOTH_EXE) $(abspath $(filter-out $< $(NUMBER_POINTS_SMOOTH_FILE), $^)) $(abspath $@) $(NB_POINTS_SMOOTH)

# Simply copies the position data to the smoothed data folder, as the position data is already smooth
$(SMOOTH_DATA_FOLDER)/%/$(POSITION_FILE_NAME): $(addprefix $(TEST_DATA_FOLDER)/, %/$(POSITION_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@cp $< $@

.PHONY: stress_strain
stress_strain: $(STRESS_STRAIN_FILES) ## Computes the stress and the strain from the position and effort files, and saves them to a .csv file for each test

$(STRESS_STRAIN_DATA_FOLDER)/%.csv: $(STRESS_STRAIN_EXE_FILE) $(addprefix $(SMOOTH_DATA_FOLDER)/, %/$(POSITION_FILE_NAME)) $(addprefix $(SMOOTH_DATA_FOLDER)/, %/$(EFFORT_FILE_NAME)) $(NOTES_FILE)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(STRESS_STRAIN_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

.PHONY: max_points
max_points: $(MAXIMUM_POINTS_FILE) ## Detects the ultimate strength and the extensibility from the stress-strain data for each test, and saves the values to a .csv file

$(MAXIMUM_POINTS_FILE): $(MAXIMUM_POINT_EXE_FILE) $(STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(MAXIMUM_POINT_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: begin
begin: $(BEGIN_FILE) ## Detects the begin extension of the valid stress-strain data for each test, and saves it to a .csv file

$(BEGIN_FILE): $(BEGIN_EXE_FILE) $(MAXIMUM_POINTS_FILE) $(STRESS_STRAIN_FILES) $(STRESS_THRESHOLD_FILE)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(BEGIN_EXE) $(abspath $@) $(STRESS_THRESHOLD) $(abspath $(filter-out $< $(STRESS_THRESHOLD_FILE), $^))

.PHONY: end
end: $(END_FILE) ## Detects the end extension of the valid stress-strain data for each test, and saves it to a .csv file

$(END_FILE): $(END_EXE_FILE) $(BEGIN_FILE) $(MAXIMUM_POINTS_FILE) $(NUMBER_POINTS_BEGIN_END_FILE) $(DROP_THRESHOLD_FILE) $(STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(END_EXE) $(abspath $@) $(NB_POINTS_SMOOTH_END) $(DROP_THRESHOLD) $(DROP_RANGE) $(BEGIN_FILE) $(MAXIMUM_POINTS_FILE) $(abspath $(filter-out $< $(BEGIN_FILE) $(MAXIMUM_POINTS_FILE) $(NUMBER_POINTS_BEGIN_END_FILE) $(DROP_THRESHOLD_FILE), $^))

.PHONY: trim
trim: $(TRIMMED_STRESS_STRAIN_FILES) ## Takes the stress-strain data as an input, and saves only the valid part of it to a .csv file for each test

$(TRIMMED_STRESS_STRAIN_DATA_FOLDER)/%.csv: $(TRIM_EXE_FILE) $(STRESS_STRAIN_DATA_FOLDER)/%.csv $(BEGIN_FILE) $(END_FILE)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(TRIM_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: yeoh_interpolation
yeoh_interpolation: $(YEOH_INTERPOLATION_FILE) ## Fits a second-order Yeoh model to the valid stress-strain data for each test, and saves the parameters to a .csv file

$(YEOH_INTERPOLATION_FILE): $(YEOH_EXE_FILE) $(TRIMMED_STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(YEOH_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: tangent_moduli
tangent_moduli: $(TANGENT_MODULI_FILE) ## Calculates the tangent moduli at both ends of the valid stress-strain data for each test, and saves the slopes to a .csv file

$(TANGENT_MODULI_FILE): $(TANGENT_MODULI_EXE_FILE) $(MODULI_RANGES_FILE) $(TRIMMED_STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(TANGENT_MODULI_EXE) $(abspath $@) $(YOUNG_RANGE) $(HYPERELASTIC_RANGE) $(abspath $(filter-out $< $(MODULI_RANGES_FILE), $^))

$(RESULTS_FILE): $(RESULTS_EXE_FILE) $(NOTES_FILE) $(BEGIN_FILE) $(END_FILE) $(MAXIMUM_POINTS_FILE) $(YEOH_INTERPOLATION_FILE) $(TANGENT_MODULI_FILE)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(RESULTS_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

.PHONY: raw_plots
raw_plots: $(RAW_PLOTS_EFFORT_FILES) $(RAW_PLOTS_POSITION_FILES) ## Plots the raw data points in .tiff files for each test

$(RAW_PLOTS_EFFORT_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(addprefix $(TEST_DATA_FOLDER)/, %/$(EFFORT_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

$(RAW_PLOTS_POSITION_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(addprefix $(TEST_DATA_FOLDER)/, %/$(POSITION_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

.PHONY: smooth_plots
smooth_plots: $(SMOOTH_PLOTS_EFFORT_FILES) $(SMOOTH_PLOTS_POSITION_FILES) ## Plots the smoothed data points in .tiff files for each test

$(SMOOTH_PLOTS_EFFORT_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(addprefix $(SMOOTH_DATA_FOLDER)/, %/$(EFFORT_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

$(SMOOTH_PLOTS_POSITION_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(addprefix $(SMOOTH_DATA_FOLDER)/, %/$(POSITION_FILE_NAME))
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

.PHONY: begin_end_plots
begin_end_plots: $(BEGIN_END_PLOTS_FILES) ## Plots the stress_strain data in .tiff files for each test, with vertical lines indicating the begin and end cutoff extension

$(BEGIN_END_PLOTS_FOLDER)/%.tiff: $(BEGIN_END_CURVE_EXE_FILE) $(STRESS_STRAIN_DATA_FOLDER)/%.csv $(BEGIN_FILE) $(END_FILE)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(BEGIN_END_CURVE_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: stress_strain_plots
stress_strain_plots: $(STRESS_STRAIN_PLOTS_FILES) $(ALL_STRESS_STRAIN_CURVES) $(ALL_STRESS_STRAIN_CURVES_TRIMMED) ## Plots the stress-strain data in .tiff files for each test, as well a one .tiff file of all the stress-strain data and one .tiff file of all the trimmed stress-strain data

$(STRESS_STRAIN_PLOTS_FOLDER)/%.tiff: $(SAVE_CURVE_EXE_FILE) $(STRESS_STRAIN_DATA_FOLDER)/%.csv
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(SAVE_CURVE_EXE) $(abspath $(filter-out $<, $^)) $(abspath $@)

$(ALL_STRESS_STRAIN_CURVES): $(ALL_STRESS_STRAIN_EXE_FILE) $(NOTES_FILE) $(STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(ALL_STRESS_STRAIN_EXE) $(abspath $(word 2,$^)) $(abspath $@) $(abspath $(filter-out $< $(NOTES_FILE), $^))

$(ALL_STRESS_STRAIN_CURVES_TRIMMED): $(ALL_STRESS_STRAIN_EXE_FILE) $(NOTES_FILE) $(TRIMMED_STRESS_STRAIN_FILES)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(ALL_STRESS_STRAIN_EXE) $(abspath $(word 2,$^)) $(abspath $@) $(abspath $(filter-out $< $(NOTES_FILE), $^))

.PHONY: yeoh_interpolation_plots
yeoh_interpolation_plots: $(INTERPOLATION_PLOTS_FILES) ## Plots the valid stress-strain data in a .tiff file for each test, with the fit of the Yeoh model superimposed

$(INTERPOLATION_CURVES_FOLDER)/%.tiff: $(INTERPOLATED_CURVE_EXE_FILE) $(TRIMMED_STRESS_STRAIN_DATA_FOLDER)/%.csv $(YEOH_INTERPOLATION_FILE)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(INTERPOLATED_CURVE_EXE) $(abspath $@) $(abspath $(filter-out $<, $^))

.PHONY: tangent_moduli_plots
tangent_moduli_plots: $(TANGENT_MODULI_PLOTS_FILES) ## Plots the valid stress-strain data in a .tiff file for each test, with the fit of the tangent moduli superimposed

$(TANGENT_MODULI_CURVES_FOLDER)/%.tiff: $(TANGENT_MODULI_CURVE_EXE_FILE) $(MODULI_RANGES_FILE) $(TRIMMED_STRESS_STRAIN_DATA_FOLDER)/%.csv $(TANGENT_MODULI_FILE)
	@mkdir -p $(@D)
	@echo "Writing $(abspath $@)"
	@$(TANGENT_MODULI_CURVE_EXE) $(abspath $@) $(YOUNG_RANGE) $(HYPERELASTIC_RANGE) $(abspath $(filter-out $< $(MODULI_RANGES_FILE), $^))

endif
