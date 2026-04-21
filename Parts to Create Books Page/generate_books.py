import re
from html import escape

INPUT_FILE = "books.txt"
OUTPUT_FILE = "books.html"

# ---------- HTML ----------
HTML_START = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catholic Library</title>
<style>
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  background:#ffe888;margin:0;padding:20px;color:#1c1c1e
}
.container{
  max-width:900px;margin:auto;background:#fff;border-radius:16px;
  padding:24px;box-shadow:0 8px 20px rgba(0,0,0,.08)
}
.library{display:flex;flex-direction:column}
.book{
  display:block;
  background:#f2f2f7;
  border-radius:10px;
  padding:14px 16px;
  margin-bottom:10px;   /* ✅ uniform spacing */
  text-decoration:none;
  color:#000
}
.book:hover{background:#e6e6eb}
.title{font-size:15px;font-weight:600}
</style>
</head>
<body>
<div class="container">
<h1>Catholic Library</h1>
<div class="library">
"""

HTML_END = """
</div>
</div>
</body>
</html>
"""

# ---------- REGEX ----------
url_re = re.compile(r"https?://[^\s\)\]]+")
html_tag_re = re.compile(r"<[^>]+>")

seen_urls = set()
books = []

current_title = "Unknown title"

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            continue

        # Strip HTML
        clean = html_tag_re.sub("", line)

        # Update title (non-URL lines)
        if not clean.startswith("http"):
            clean = url_re.sub("", clean).strip(" –:-")
            if clean:
                current_title = clean

        # Extract URLs
        for url in url_re.findall(line):
            if url in seen_urls:
                continue  # ✅ de-duplicate
            seen_urls.add(url)
            books.append((escape(current_title), url))

# ---------- WRITE OUTPUT ----------
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(HTML_START)
    for title, url in books:
        out.write(
            f'<a class="book" href="{url}" target="_blank">\n'
            f'  <div class="title">{title}</div>\n'
            f'</a>\n'
        )
    out.write(HTML_END)

print(f"✅ Generated {len(books)} unique books into {OUTPUT_FILE}")
