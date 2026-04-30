#!/bin/bash
set -e

echo "Starting inference..."

# 检查目录
[ -d "/saisdata" ] || { echo "Error: /saisdata not found"; exit 1; }
[ -d "/saisresult" ] || { echo "Error: /saisresult not found"; exit 1; }

# 运行推理
python /app/src/run_inference.py

# 检查输出
[ -f "/saisresult/prediction.json" ] || { echo "Error: prediction.json not found"; exit 1; }

echo "Done!"