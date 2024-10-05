IMAGE_NAME=tripit

.PHONY: usage
usage:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  clean       Remove all generated files"
	@echo "  ruff        Run ruff format and check"
	@echo "  build       Build the project"
	@echo "  trips       Run tripit-tools trips"
	@echo "  profiles    Run tripit-tools profiles"
	@echo "  image       Build the container image"
	@echo "  push        Push the container image to the registry"
	@echo

.PHONY: clean
clean:
	@git clean -Xdf
	@if podman images -q $$DEV_REGISTRY/$(IMAGE_NAME) | grep -q .; then \
		podman rmi -f $$(podman images -q $$DEV_REGISTRY/$(IMAGE_NAME)); \
	fi

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


# Docker image build and push

.PHONY: image
image: sync
	@podman build --build-arg VERSION=$$(uv run --quiet hatchling version) -t $$DEV_REGISTRY/$(IMAGE_NAME):$$(uv run --quiet hatchling version | sed "s|\+.*||") --format=docker .

.PHONY: push
push: image
	@podman push $$DEV_REGISTRY/$(IMAGE_NAME):$$(uv run --quiet hatchling version | sed "s|\+.*||")

# PyPi package build and upload

.PHONY: build
build: sync
	@uv build

.PHONY: test-upload
test-upload: build
	@UV_PUBLISH_URL=https://test.pypi.org/legacy/ uv publish
