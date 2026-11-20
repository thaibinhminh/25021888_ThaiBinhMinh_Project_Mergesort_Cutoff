import os
import pandas as pd
from docx import Document
from docx.shared import Inches

def replace_in_paragraph(p, mapping):
    full_text = "".join(run.text for run in p.runs)
    changed = False
    for k, v in mapping.items():
        if k in full_text:
            full_text = full_text.replace(k, str(v))
            changed = True
    if changed and p.runs:
        p.runs[0].text = full_text
        for r in p.runs[1:]:
            r.text = ""

def main():
    template_path = "../1_BaoCao_ThiNghiem/25021888_ThaiBinhMinh_BaoCao_ThiNghiem_CUTOFF.docx"
    output_path = "../1_BaoCao_ThiNghiem/25021888_ThaiBinhMinh_BaoCao_ThiNghiem_CUTOFF_HoanChinh.docx"

    if not os.path.exists("summary_stats.csv"):
        raise FileNotFoundError("Khong tim thay summary_stats.csv! Hay chay analyze_and_plot.py truoc.")

    summary = pd.read_csv("summary_stats.csv")
    max_n = summary["N"].max()
    mapping = {}

    # Điền Bảng 1 (Random tại max_n)
    rand_df = summary[(summary["N"] == max_n) & (summary["Distribution"] == "Random")]
    for _, row in rand_df.iterrows():
        c = int(row["Cutoff"])
        mapping[f"{{{{R_{c}_MEAN}}}}"] = f"{row['Mean_ms']:.3f}"
        mapping[f"{{{{R_{c}_MED}}}}"] = f"{row['Median_ms']:.3f}"
        mapping[f"{{{{R_{c}_STD}}}}"] = f"{row['Std_ms']:.3f}"
        mapping[f"{{{{R_{c}_CI}}}}"] = f"{row['CI95_ms']:.3f}"
        mapping[f"{{{{R_{c}_SP}}}}"] = f"{row['Speedup_pct']:.2f}"

    # Điền Bảng 2 (Tối ưu theo từng phân phối tại max_n)
    for dist in ["Random", "Sorted", "Reverse", "NearlySorted"]:
        sub = summary[(summary["N"] == max_n) & (summary["Distribution"] == dist)]
        best_row = sub.loc[sub["Mean_ms"].idxmin()]
        t7 = sub[sub["Cutoff"] == 7]["Mean_ms"].values[0]
        t10 = sub[sub["Cutoff"] == 10]["Mean_ms"].values[0]
        mapping[f"{{{{D_{dist}_BEST_C}}}}"] = str(int(best_row["Cutoff"]))
        mapping[f"{{{{D_{dist}_BEST_T}}}}"] = f"{best_row['Mean_ms']:.3f}"
        mapping[f"{{{{D_{dist}_T7}}}}"] = f"{t7:.3f}"
        mapping[f"{{{{D_{dist}_T10}}}}"] = f"{t10:.3f}"
        mapping[f"{{{{D_{dist}_SP}}}}"] = f"{best_row['Speedup_pct']:.2f}"

    doc = Document(template_path)

    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    replace_in_paragraph(p, mapping)

    img_map = {
        "{{FIG1_PLACEHOLDER}}": ("fig1_cutoff_curve_random.png", Inches(6.3)),
        "{{FIG2_PLACEHOLDER}}": ("fig2_distributions_comparison.png", Inches(5.8)),
        "{{FIG3_PLACEHOLDER}}": ("fig3_speedup_bar.png", Inches(5.8)),
    }

    for p in doc.paragraphs:
        inserted = False
        for tag, (img_file, width) in img_map.items():
            if tag in p.text and os.path.exists(img_file):
                p.text = ""
                run = p.add_run()
                run.add_picture(img_file, width=width)
                inserted = True
                break
        if not inserted:
            replace_in_paragraph(p, mapping)

    doc.save(output_path)
    print(f"Da xuat bao cao hoan chinh tai: {output_path}")

if __name__ == "__main__":
    main()
