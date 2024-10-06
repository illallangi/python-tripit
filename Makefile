.PHONY: usage
usage:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  clean       Remove all generated files"
	@echo "  ruff        Run ruff format and check"
	@echo "  build       Build the project"
	@echo "  flights     Run tripit-tools flights"
	@echo "  profiles    Run tripit-tools profiles"
	@echo "  trips       Run tripit-tools trips"
	@echo

.PHONY: clean
clean:
	@git clean -Xdf
4
.PHONY: ruff
ruff:
	@uv run --quiet ruff format src
	@uv run --quiet ruff check src

.PHONY: sync
sync: ruff
	@uv sync --quiet

.PHONY: commit
commit: sync
	@uv run --quiet cz commit

# Shortcuts to run the tripit-tools command

.PHONY: help
help: sync
	@uv run --quiet tripit-tools --help

.PHONY: version
version: sync
	@uv run --quiet tripit-tools --version

.PHONY: flights
flights: sync
	@uv run --quiet tripit-tools flights

.PHONY: flights.json
flights.json: sync
	@uv run --quiet tripit-tools flights --json | jq > $@

.PHONY: profiles
profiles: sync
	@uv run --quiet tripit-tools profiles

.PHONY: profiles.json
profiles.json: sync
	@uv run --quiet tripit-tools profiles --json | jq > $@

.PHONY: trips
trips: sync
	@uv run --quiet tripit-tools trips

.PHONY: trips.json
trips.json: sync
	@uv run --quiet tripit-tools trips --json | jq > $@

# PyPi package build and upload

.PHONY: build
build: sync
	@uv build

.PHONY: test-upload
test-upload: build
	@UV_PUBLISH_URL=https://test.pypi.org/legacy/ uv publish
