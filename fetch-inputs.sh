#!/usr/bin/env bash
set -euo pipefail

if [ -z "${AOC_SESSION:-}" ]; then
  echo "AOC_SESSION environment variable is not set" >&2
  exit 1
fi

cd "$(dirname "$0")"

for day_dir in */; do
  day="${day_dir%/}"
  if [[ "$day" =~ ^[0-9]+$ ]]; then
    input_file="$day/input"
    if [ ! -s "$input_file" ]; then
      echo "Fetching day $day"
      curl -sf --cookie "session=$AOC_SESSION" \
        -A "github.com/J0s3f/aoc2022 personal script" \
        "https://adventofcode.com/2022/day/$day/input" -o "$input_file"
      sleep 1
    fi
  fi
done
