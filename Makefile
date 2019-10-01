.DEFAULT_GOAL := all
.REPORTS_DIR := reports
.PYTHON_ENV_DIR := env

SHELL := /bin/bash
PATH  := $(.PYTHON_ENV_DIR)/bin:bin:$(PATH)

$(.PYTHON_ENV_DIR):
	@virtualenv --python=$(which python3) $@
	@source $@/bin/activate; pip install -r requirements.txt;

$(.REPORTS_DIR):
	@mkdir $@

.PHONY: report-designkits
report-designkits: $(.PYTHON_ENV_DIR) $(.REPORTS_DIR)
	@source activate; \
		report_designkits.py;

.PHONY: report-js-languages
report-js-languages: $(.PYTHON_ENV_DIR) $(.REPORTS_DIR)
	@source activate; \
		report_js_languages.py;

.PHONY: report-node-apps
report-node-apps: $(.PYTHON_ENV_DIR) $(.REPORTS_DIR)
	@source activate; \
		report_node_apps.py;

.PHONY: js-apps-snyk-report
js-apps-snyk-report: $(.PYTHON_ENV_DIR) $(.REPORTS_DIR)
	@source activate; \
		report_js_apps_snyk.py;

.PHONY: clean
clean:
	@rm $(.REPORTS_DIR)/*.json

.PHONY: all
all: report-designkits report-js-languages report-node-apps js-apps-snyk-report
