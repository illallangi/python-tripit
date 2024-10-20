.PHONY: usage
usage:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  clean       Remove all generated files"
	@echo "  lint        Run ruff format, check and uv sync"
	@echo "  commit      Run cz commit"
	@echo "  build       Build the project"
	@echo
	@echo "  help        Run tripit-tools help"
	@echo "  version     Run tripit-tools version"
	@echo "  flights     Run tripit-tools flights"
	@echo "  profiles    Run tripit-tools profiles"
	@echo "  trips       Run tripit-tools trips"
	@echo

.PHONY: clean
clean:
	@git clean -Xdf
	@mkdir -p .git/hooks
	@rm -f .git/hooks/*.sample
	@find .git/hooks/ -type f  | while read i; do chmod +x $$i; done

.PHONY: lint
lint:
	@uv run --quiet deptry src --experimental-namespace-package
	@uv run --quiet ruff format src
	@uv run --quiet ruff check src --quiet
	@uv sync --quiet

.PHONY: commit
commit: lint
	@uv run --quiet cz commit

.PHONY: build
build: lint
	@uv build


.PHONY: help
help: lint
	@uv run --quiet tripit-tools --help

.PHONY: version
version: lint
	@uv run --quiet tripit-tools --version

.PHONY: flights
flights: lint
	@uv run --quiet tripit-tools flights

.PHONY: flights.json
flights.json: lint
	@uv run --quiet tripit-tools flights --json | jq > $@

.PHONY: profiles
profiles: lint
	@uv run --quiet tripit-tools profiles

.PHONY: profiles.json
profiles.json: lint
	@uv run --quiet tripit-tools profiles --json | jq > $@

.PHONY: trips
trips: lint
	@uv run --quiet tripit-tools trips

.PHONY: trips.json
trips.json: lint
	@uv run --quiet tripit-tools trips --json | jq > $@
