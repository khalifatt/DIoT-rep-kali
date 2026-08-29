#!/usr/bin/env bash
set -e

echo "[*] Initializing Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[*] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Executing unit test suite..."
python3 -m unittest discover -s tests

echo "[*] Generating 500-node testbed schema graph..."
python3 src/pcm_graph_builder.py

echo "[*] Computing evaluation metrics (TPR, FPR, F1, AUC)..."
python3 src/eval_metrics.py

echo "[*] Artifact evaluation pipeline completed successfully."
