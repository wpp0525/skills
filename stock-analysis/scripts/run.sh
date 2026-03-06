#!/bin/bash
# Stock Analysis Runner - Linux/macOS
# This script runs the stock analysis directly using local Python

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if stock code is provided
if [ -z "$1" ]; then
    echo "Usage: ./run.sh <stock_code>"
    echo "Example: ./run.sh 000001"
    exit 1
fi

# Run the analysis (pass current directory as output directory)
python "$SCRIPT_DIR/analyze_stock.py" "$1" --output-dir "$(pwd)"
