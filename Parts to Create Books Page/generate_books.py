import re
from html import escape

INPUT_FILE = "books.txt"
OUTPUT_FILE = "books.html"

HTML_START = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catholic Library</title>

<style>
* { box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  background: #ffe888;
  margin: 0;
  padding: 20px;
  color: #1c1c1e;
}

.container {
  max-width: 900px;
  margin: auto;
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 20px rgba(0,0,0,.08);
}

.search-wrapper {
  position: relative;
  margin-bottom: 16px;
}

.search-wrapper input {
  width: 100%;
  padding: 12px 42px 12px 14px;
  font-size: 15px;
  border-radius: 10px;
  border: 1px solid #ccc;
}

.search-wrapper button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: none;
  font-size: 20px;
  cursor: pointer;
  display: none;
}

.library {
  display: flex;
  flex-direction: column;
}

.book {
  display: block;
  background: #f2f2f7;
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
  text-decoration: none;
  color: #000;
}

.book:hover {
  background: #e6e6eb;
}

.title {
  font-size: 15px;
  font-weight: 600;
}

mark {
  background: #ffeb3b;
}
</style>
</head>

<body>
<div class="container">
  <h1>Catholic Library</h1>

  <div class="search-wrapper">
    <input id="searchInput" placeholder="Search books..." oninput="filterBooks()">
    <button id="clearBtn" onclick="clearSearch()">×</button>
  </div>

  <div class="library">
"""

HTML_END = """
  </div>
</div>

<script>
function filterBooks() {
  const q = searchInput.value.toLowerCase();
  clearBtn.style.display = q ? "block" : "none";

  document.querySelectorAll(".book").forEach(b => {
    const t = b.querySelector(".title");
    const text = t.textContent;
    t.innerHTML = text;

    if (text.toLowerCase().includes(q)) {
      b.style.display = "";
      if (q) {
        t.innerHTML = text.replace(
          new RegExp("(" + q.replace(/[.*+?^${}()|[\\]\\\\]/g,"\\\\$&") + ")", "ig"),
          "<mark>$1</mark>"
        );
      }
    } else {
      b.style.display = "none";
    }
  });
}

function clearSearch() {
  searchInput.value = "";
  clearBtn.style.display = "none";
  filterBooks();
}
</script>

</body>
</html>
"""

# ---------- PARSING ----------
url_re = re.compile(r"https?://[^\s\)\]]+")
html_re = re.compile(r"<[^>]+>")

seen = set()
books = []
current_title = None

def is_youtube(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        clean = html_re.sub("", line)

        if not clean.startswith("http"):
            clean = url_re.sub("", clean).strip(" –:-")
            if clean:
                current_title = clean

        for url in url_re.findall(line):
            if is_youtube(url):
                continue  # ✅ skip YouTube links
            if url not in seen and current_title:
                seen.add(url)
                books.append((escape(current_title), url))

# ---------- WRITE FILE ----------
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(HTML_START)
    for title, url in books:
        out.write(
            f'<a class="book" href="{url}" target="_blank">\n'
            f'  <div class="title">{title}</div>\n'
            f'</a>\n'
        )
    out.write(HTML_END)

print(f"✅ Generated {len(books)} unique books (YouTube excluded) into {OUTPUT_FILE}")
