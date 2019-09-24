SHELL=/bin/bash
.DEFAULT_GOAL := all
.REPORTS_DIR := reports
.BIN := ./bin
.PYTHON_ENV_DIR := env

$(.PYTHON_ENV_DIR):
	@virtualenv --python=$(which python3) $@
	@source $@/bin/activate; pip install -r requirements.txt;

$(.REPORTS_DIR):
	@mkdir $@

.PHONY: report-designkits
report-designkits: $(.PYTHON_ENV_DIR) $(.REPORTS_DIR)
	@source $(.PYTHON_ENV_DIR)/bin/activate; \
		$(.BIN)/report_designkits.py;

.PHONY: report-js-languages
report-js-languages: $(.PYTHON_ENV_DIR) $(.REPORTS_DIR)
	@source $(.PYTHON_ENV_DIR)/bin/activate; \
		$(.BIN)/report_js_languages.py;

.PHONY: report-node-apps
report-node-apps: $(.PYTHON_ENV_DIR) $(.REPORTS_DIR)
	@source $(.PYTHON_ENV_DIR)/bin/activate; \
		$(.BIN)/report_node_apps.py;

.PHONY: all
all: report-designkits report-js-languages report-node-apps
