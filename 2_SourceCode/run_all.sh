#!/usr/bin/env bash
set -e
echo "[1/4] Bien dich Java..."
javac -encoding UTF-8 MergeCutoff.java ExperimentRunner.java
echo "[2/4] Chay thi nghiem do thoi gian..."
java -Xms2g -Xmx2g ExperimentRunner
echo "[3/4] Phan tich thong ke va ve bieu do..."
python3 analyze_and_plot.py
echo "[4/4] Tu dong dien so lieu vao file Bao cao Word..."
python3 auto_fill_report.py
echo "HOAN TAT!"
