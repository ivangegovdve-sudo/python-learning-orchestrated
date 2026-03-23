#!/usr/bin/env bash

# Text formatting
CYAN="\033[0;36m"
YELLOW="\033[1;33m"
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m" # No Color

echo -e "${CYAN}Starting Python Learning App...${NC}"

echo -e "${YELLOW}Syncing dependencies...${NC}"
if ! uv sync --group dev; then
    echo -e "${RED}Error syncing dependencies. Make sure 'uv' is installed.${NC}"
    read -p "Press Enter to quit..."
    kill -INT $$
fi

echo -e "${GREEN}Launching app...${NC}"
if ! uv run python-learning session; then
    read -p "Press Enter to quit..."
    kill -INT $$
fi
