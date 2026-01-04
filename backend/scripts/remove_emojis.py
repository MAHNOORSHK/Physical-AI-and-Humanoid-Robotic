"""
Remove emojis from markdown files
"""
import re
from pathlib import Path

def remove_emojis(text):
    """Remove emojis from text"""
    # Pattern to match emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def process_markdown_files():
    """Process all markdown files and remove emojis"""
    docs_dir = Path(__file__).parent.parent.parent / "frontend" / "docs"
    md_files = list(docs_dir.rglob("*.md"))

    print(f"Found {len(md_files)} markdown files\n")

    total_emojis_removed = 0

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count emojis before removal
        emojis_before = len(content)
        cleaned_content = remove_emojis(content)
        emojis_after = len(cleaned_content)
        emojis_removed = emojis_before - emojis_after

        if emojis_removed > 0:
            # Write cleaned content back
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            print(f"[OK] {md_file.name}: Removed {emojis_removed} emoji characters")
            total_emojis_removed += emojis_removed

    print(f"\n[DONE] Total emoji characters removed: {total_emojis_removed}")

if __name__ == "__main__":
    process_markdown_files()
