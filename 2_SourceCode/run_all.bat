@echo off
chcp 65001 > nul
echo =================================================================
echo  CHAY TU DONG THI NGHIEM MERGESORT CUTOFF - THAI BINH MINH (UET)
echo =================================================================
echo [1/4] Bien dich Java...
javac -encoding UTF-8 MergeCutoff.java ExperimentRunner.java
if errorlevel 1 (
    echo Loi bien dich Java! Vui long kiem tra JDK.
    pause
    exit /b 1
)

echo [2/4] Chay thi nghiem do thoi gian (~1 phut)...
java -Xms2g -Xmx2g ExperimentRunner

echo [3/4] Phan tich thong ke va ve 3 bieu do khoa hoc...
python analyze_and_plot.py

echo [4/4] Tu dong dien so lieu & bieu do vao file Bao cao Word...
python auto_fill_report.py

echo =================================================================
echo HOAN TAT! Mo thu muc 1_BaoCao_ThiNghiem de xem file Word hoan chinh.
pause
