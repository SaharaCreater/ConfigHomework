#!/usr/bin/env bash
set -e

if [ $# -eq 0 ]; then
    python3 -m src.cli -i examples/server_config.conf
else
    python3 -m src.cli "$@"
fi
