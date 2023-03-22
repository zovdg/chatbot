#!/bin/bash
# entrypoint.sh file of Dockerfile

# Section1: Bash options
set -o errexit
set -o pipefail
set -o nounset

exec start.sh "$@"
