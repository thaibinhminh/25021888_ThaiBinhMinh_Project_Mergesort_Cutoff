import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    if not os.path.exists("results.csv"):
        raise FileNotFoundError("Khong tim thay results.csv! Hay chay ExperimentRunner truoc.")

    df = pd.read_csv("results.csv")

    summary = (
        df.groupby(["N", "Distribution", "Cutoff"])["TimeMs"]
        .agg(
            Trials="count",
            Mean_ms="mean",
            Median_ms="median",
            Std_ms="std",
            Min_ms="min",
            Max_ms="max",
        )
        .reset_index()
    )

    summary["CI95_ms"] = 1.96 * summary["Std_ms"] / np.sqrt(summary["Trials"])

    baseline = summary[summary["Cutoff"] == 1][["N", "Distribution", "Mean_ms"]].rename(
        columns={"Mean_ms": "Baseline_ms"}
    )
    summary = summary.merge(baseline, on=["N", "Distribution"])
    summary["Speedup_pct"] = (
        (summary["Baseline_ms"] - summary["Mean_ms"]) / summary["Baseline_ms"]
    ) * 100.0

    summary.to_csv("summary_stats.csv", index=False)

    best_rows = summary.loc[summary.groupby(["N", "Distribution"])["Mean_ms"].idxmin()]
    print("\n=== BANG CUTOFF TOI UU THEO TUNG KICH THUOC & PHAN PHOI ===")
    print(
        best_rows[
            ["N", "Distribution", "Cutoff", "Mean_ms", "Median_ms", "Std_ms", "CI95_ms", "Speedup_pct"]
        ].to_string(index=False)
    )

    max_n = df["N"].max()
    print(f"\n=== BANG CHI TIET TAI N = {max_n:,} (DU LIEU RANDOM) ===")
    rand_max = summary[(summary["N"] == max_n) & (summary["Distribution"] == "Random")]
    print(
        rand_max[
            ["Cutoff", "Mean_ms", "Median_ms", "Std_ms", "CI95_ms", "Speedup_pct"]
        ].to_string(index=False)
    )

    plt.style.use("seaborn-v0_8-whitegrid")

    # HÌNH 1: Đường cong thời gian thực thi trên 3 quy mô N (Random)
    sizes = sorted(df["N"].unique())
    fig, axes = plt.subplots(1, len(sizes), figsize=(15, 4.8), dpi=300)
    if len(sizes) == 1:
        axes = [axes]

    for ax, n in zip(axes, sizes):
        sub = summary[(summary["N"] == n) & (summary["Distribution"] == "Random")].sort_values("Cutoff")
        ax.errorbar(
            sub["Cutoff"],
            sub["Mean_ms"],
            yerr=sub["CI95_ms"],
            fmt="-o",
            capsize=3,
            linewidth=1.8,
            markersize=5,
            color="#004A8F",
            label="Mean ± 95% CI",
        )
        best_c = int(sub.loc[sub["Mean_ms"].idxmin(), "Cutoff"])
        ax.axvline(7, color="#ff7f0e", linestyle="--", linewidth=1.2, label="CUTOFF = 7 (Cũ)")
        ax.axvline(10, color="#2ca02c", linestyle="-.", linewidth=1.2, label="CUTOFF = 10 (Mới)")
        ax.axvline(best_c, color="#d62728", linestyle=":", linewidth=1.6, label=f"Tối ưu = {best_c}")

        ax.set_title(f"Random — N = {n:,}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Giá trị CUTOFF")
        ax.set_ylabel("Thời gian trung bình (ms)")
        ax.legend(fontsize=8, loc="upper right")

    plt.suptitle("Ảnh hưởng của CUTOFF đến thời gian chạy Mergesort (ASUS TUF F15 — i5-11400H)", fontsize=13, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig("fig1_cutoff_curve_random.png")
    plt.close()

    # HÌNH 2: Thời gian chuẩn hóa trên 4 phân phối dữ liệu tại N lớn nhất
    plt.figure(figsize=(10, 5.8), dpi=300)
    for dist in summary["Distribution"].unique():
        sub = summary[(summary["N"] == max_n) & (summary["Distribution"] == dist)].sort_values("Cutoff")
        norm_time = sub["Mean_ms"] / sub["Baseline_ms"]
        plt.plot(sub["Cutoff"], norm_time, marker="o", markersize=4.5, linewidth=1.8, label=dist)

    plt.axhline(1.0, color="black", linestyle="--", linewidth=1, label="Baseline (CUTOFF = 1)")
    plt.axvline(7, color="gray", linestyle=":", linewidth=1)
    plt.axvline(10, color="gray", linestyle="-.", linewidth=1)
    plt.title(f"Tỷ số thời gian chuẩn hóa (T_cutoff / T_baseline) trên 4 phân phối (N = {max_n:,})", fontsize=12.5, fontweight="bold")
    plt.xlabel("Giá trị CUTOFF")
    plt.ylabel("Tỷ số thời gian so với CUTOFF = 1")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fig2_distributions_comparison.png")
    plt.close()

    # HÌNH 3: Biểu đồ cột so sánh % tăng tốc
    plt.figure(figsize=(10, 5.4), dpi=300)
    dists = list(summary["Distribution"].unique())
    x = np.arange(len(dists))
    width = 0.25

    sp_7 = [summary[(summary["N"] == max_n) & (summary["Distribution"] == d) & (summary["Cutoff"] == 7)]["Speedup_pct"].values[0] for d in dists]
    sp_10 = [summary[(summary["N"] == max_n) & (summary["Distribution"] == d) & (summary["Cutoff"] == 10)]["Speedup_pct"].values[0] for d in dists]
    sp_best = [summary[(summary["N"] == max_n) & (summary["Distribution"] == d)]["Speedup_pct"].max() for d in dists]

    plt.bar(x - width, sp_7, width, label="CUTOFF = 7 (Giáo trình cũ)", color="#ff7f0e")
    plt.bar(x, sp_10, width, label="CUTOFF = 10 (Giáo trình mới)", color="#2ca02c")
    plt.bar(x + width, sp_best, width, label="Tối ưu thực nghiệm trên máy", color="#d62728")

    plt.xticks(x, dists)
    plt.ylabel("Mức tăng tốc so với CUTOFF = 1 (%)")
    plt.title(f"So sánh hiệu quả tăng tốc (%) tại N = {max_n:,}", fontsize=12.5, fontweight="bold")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fig3_speedup_bar.png")
    plt.close()

    print("\nDa xuat thanh cong summary_stats.csv va 3 bieu do PNG!")

if __name__ == "__main__":
    main()
