from pathlib import Path


def merge_md_files(folder: Path) -> None:
    """將 folder 底下所有 .md 遞迴合併成一個 .txt，以 folder 名稱命名。"""
    md_files = sorted(folder.rglob("*.md"))
    if not md_files:
        print(f"  ⏭ {folder.name}/ 裡沒有 .md，跳過")
        return

    output_file = folder / f"{folder.name}.txt"
    with output_file.open("w", encoding="utf-8") as out_f:
        for idx, md_path in enumerate(md_files):
            text = md_path.read_text(encoding="utf-8")
            out_f.write(text)
            if idx != len(md_files) - 1:
                out_f.write("\n\n")

    print(f"  ✅ 合併 {len(md_files)} 個 .md → {output_file}")


def main():
    raw = input("請輸入資料夾路徑：").strip()
    base_dir = Path(raw).expanduser().resolve()

    if not base_dir.is_dir():
        raise SystemExit(f"找不到資料夾：{base_dir}")

    # 找出所有直接子資料夾
    subdirs = sorted([d for d in base_dir.iterdir() if d.is_dir()])

    # 根目錄本身直接放的 .md（不含子資料夾裡的）
    root_md = sorted(base_dir.glob("*.md"))

    if not subdirs and not root_md:
        raise SystemExit(f"在 {base_dir} 裡沒有找到子資料夾或 .md 檔案")

    print(f"\n📂 目標：{base_dir}")
    print(f"   子資料夾：{len(subdirs)} 個，根目錄 .md：{len(root_md)} 個\n")

    # 1) 每個子資料夾各自合併
    for subdir in subdirs:
        merge_md_files(subdir)

    # 2) 根目錄的 .md 也合併（如果有的話）
    if root_md:
        output_file = base_dir / f"{base_dir.name}.txt"
        with output_file.open("w", encoding="utf-8") as out_f:
            for idx, md_path in enumerate(root_md):
                text = md_path.read_text(encoding="utf-8")
                out_f.write(text)
                if idx != len(root_md) - 1:
                    out_f.write("\n\n")
        print(f"  ✅ 合併 {len(root_md)} 個根目錄 .md → {output_file}")

    print("\n🎉 全部完成！")


if __name__ == "__main__":
    main()
