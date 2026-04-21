import re
import os
from urllib.parse import unquote

INPUT_FILE = "books1.txt"
OUTPUT_FILE = "books1.html"

# -------------------------------------------------
# Read file safely (UTF-8 or UTF-16)
# -------------------------------------------------
def read_lines(path):
    for enc in ("utf-8", "utf-16"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.readlines()
        except UnicodeError:
            continue
    raise RuntimeError("Could not decode input file")

lines = read_lines(INPUT_FILE)

# -------------------------------------------------
# Extract books
# -------------------------------------------------
books = []

for line in lines:
    # Extract URL inside quotes
    m = re.search(r'"(https?://[^"]+)"', line)
    if not m:
        continue

    url = m.group(1).strip()

    # Skip RTF files entirely
    if url.lower().endswith(".rtf"):
        continue

    # Build human title from URL slug
    slug = url.rstrip("/").split("/")[-1]
    slug = unquote(slug)
    slug = slug.replace("_", " ")
    title = slug.replace("-", " ").strip()

    # Format list (static, per your example)
    formats = "pdf, epub, kindle format"

    display_title = f"{title} ({formats})"

    books.append((display_title, url))

# -------------------------------------------------
# Write HTML (EXACT FORMAT)
# -------------------------------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Books Library</title>
<style>
.book {
  display: block;
  text-decoration: none;
  background: #f2f2f7;
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 10px;
  color: #000;
}
.book:hover { background: #e6e6eb; }
.title { font-size: 15px; font-weight: 600; }
</style>
</head>
<body>
""")

    for title, url in books:
        out.write(
            f'<a class="book" href="{url}" target="_blank">\n'
            f'  <div class="title">{title}</div>\n'
            f'</a>\n\n'
        )

    out.write("</body>\n</html>")

print(f"✅ Generated {len(books)} books into {OUTPUT_FILE} (RTF excluded)")
