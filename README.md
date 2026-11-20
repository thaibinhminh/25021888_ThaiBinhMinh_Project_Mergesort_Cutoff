# Thực Nghiệm Xác Định Ngưỡng CUTOFF Tối Ưu Cho Thuật Toán Mergesort

- **Sinh viên thực hiện:** Thái Bình Minh — **MSSV:** 25021888
- **Lớp môn học:** 2627I_UET.CS1058_9 — **Giảng viên hướng dẫn:** TS. Trần Thị Minh Châu
- **Môi trường thí nghiệm:** Laptop ASUS TUF Gaming F15 (Intel Core i5-11400H, RAM 8GB DDR4, IntelliJ IDEA — OpenJDK 26, Python 3)

---

## 1. Tổng quan & Mục tiêu

Dự án khảo sát thực nghiệm ảnh hưởng của ngưỡng chuyển đổi **`CUTOFF`** (từ đệ quy Top-down Mergesort sang Insertion Sort cho các mảng con kích thước nhỏ) nhằm xác định giá trị tối ưu trên kiến trúc phần cứng hiện đại và so sánh với các mốc lý thuyết kinh điển ($7$ và $10$).

Cài đặt trong `MergeCutoff.java` tuân thủ chuẩn giáo trình *Algorithms* (Sedgewick & Wayne) và bài giảng UET với 3 kỹ thuật tối ưu:
1. **Insertion Sort Cutoff:** Sắp xếp chèn tại chỗ cho các đoạn con thỏa mãn `hi <= lo + cutoff - 1`.
2. **Skip-Merge Optimization:** Bỏ qua bước trộn nếu hai nửa đã có thứ tự tự nhiên (`a[mid] <= a[mid + 1]`), giúp đạt độ phức tạp $O(N)$ trên dữ liệu đã sắp xếp.
3. **Half-size Auxiliary Array:** Cấp phát mảng phụ `aux` kích thước `N / 2 + 1`, chỉ sao chép nửa trái và giữ nguyên nửa phải tại chỗ trên mảng gốc.

---

## 2. Cấu trúc thư mục dự án

```text
25021888_ThaiBinhMinh_Project_Mergesort_Cutoff/
├── README.md
├── 1_BaoCao_ThiNghiem/
│   └── 25021888_ThaiBinhMinh_BaoCao_ThiNghiem_CUTOFF_HoanChinh.docx
├── 2_SourceCode/
│   ├── MergeCutoff.java         # Cài đặt Top-down Mergesort tối ưu (Cutoff, Skip-Merge, aux N/2)
│   ├── ExperimentRunner.java    # Sinh bộ dữ liệu, làm nóng JVM và đo thời gian thực nghiệm
│   ├── analyze_and_plot.py      # Thống kê mô tả (Mean, Median, Std, 95% CI, Speedup) & vẽ biểu đồ
│   ├── auto_fill_report.py      # Tự động điền số liệu & nhúng biểu đồ vào báo cáo Word
│   ├── run_all.bat              # Script chạy tự động toàn bộ quy trình trên Windows
│   ├── run_all.sh               # Script chạy tự động toàn bộ quy trình trên Linux / macOS
│   └── output/
│       ├── results.csv                        # Dữ liệu đo thô của toàn bộ 2.520 lượt chạy
│       ├── summary_stats.csv                  # Bảng tổng hợp thống kê theo từng cấu hình
│       ├── fig1_cutoff_curve_random.png       # Đường cong thời gian thực thi trên dữ liệu Random
│       ├── fig2_distributions_comparison.png  # So sánh hiệu năng theo 4 phân phối dữ liệu
│       └── fig3_speedup_bar.png               # Biểu đồ mức tăng tốc (%) tại CUTOFF tối ưu
├── 3_Datasets/                  # 12 tệp dữ liệu thực nghiệm cố định (SEED = 42)
│   ├── Random_N{100000,500000,1000000}.txt
│   ├── Sorted_N{100000,500000,1000000}.txt
│   ├── Reverse_N{100000,500000,1000000}.txt
│   └── NearlySorted_N{100000,500000,1000000}.txt
└── 4_AI_Chat_Log/
    └── AI_Chat_Log.pdf               # Nhật ký trao đổi và hỗ trợ nghiên cứu với AI