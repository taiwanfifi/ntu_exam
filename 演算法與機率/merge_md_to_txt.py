from pathlib import Path


def merge_md_to_txt():
    base_dir = Path(__file__).parent / "白噪音診所_小說"
    output_file = Path(__file__).parent / "白噪音診所_小說_合併輸出.txt"

    if not base_dir.is_dir():
        raise SystemExit(f"找不到資料夾：{base_dir}")

    md_files = sorted(base_dir.rglob("*.md"))

    if not md_files:
        raise SystemExit(f"在 {base_dir} 裡沒有找到任何 .md 檔案")

    with output_file.open("w", encoding="utf-8") as out_f:
        for idx, md_path in enumerate(md_files):
            text = md_path.read_text(encoding="utf-8")
            out_f.write(text)
            if idx != len(md_files) - 1:
                out_f.write("\n\n")

    print(f"已合併 {len(md_files)} 個 .md 檔案到：{output_file}")


if __name__ == "__main__":
    merge_md_to_txt()
