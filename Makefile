.DEFAULT_GOAL := all
.REPORTS_DIR := reports
.BIN := bin
.PYTHON_ENV_DIR := env

$(.PYTHON_ENV_DIR):
	@virtualenv $@
	@source $@/bin/activate
	@pip install -r requirements.txt

$(.REPORTS_DIR):
	@mkdir $@

.PHONY: report-designkits
report-designkits: $(.REPORTS_DIR)
	@$(.BIN)/report_designkits.py

.PHONY: report-js-languages
report-js-languages: $(.REPORTS_DIR)
	@$(.BIN)/report_js_languages.py

.PHONY: report-node-apps
report-node-apps: $(.REPORTS_DIR)
	@$(.BIN)/report_node_apps.py

.PHONY: all
all: report-designkits report-js-languages report-node-apps