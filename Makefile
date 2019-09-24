.DEFAULT_GOAL:= all

.PHONY: report-designkits
report-designkits:
	@python report_designkits.py

.PHONY: report-js-languages
report-js-languages:
	@python report_js_languages.py

.PHONY: report-node-apps
report-node-apps:
	@python report_node_apps.py

.PHONY: all
all: report-designkits report-js-languages report-node-apps