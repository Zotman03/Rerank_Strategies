import json, html, sys

if len(sys.argv) != 3:
    print("Usage: python script.py <input_json> <output_html>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

html_parts = []

html_parts.append("""
<html>
<head>
<meta charset="UTF-8">
<title>Reranked Results</title>
<style>
body { font-family: Arial; margin: 40px; }
.result { border:1px solid #ccc; padding:15px; margin-bottom:20px; }
.content { white-space: pre-wrap; background:#f7f7f7; padding:10px; }
.metadata { background:#fafafa; padding:10px; margin-top:10px; }
</style>
</head>
<body>
<h1>Reranked Retrieval Results</h1>
""")

for r in data:
    metadata_html = "<br>".join(
        f"<b>{html.escape(k)}</b>: {html.escape(str(v))}"
        for k, v in r["metadata"].items()
    )

    html_parts.append(f"""
<div class="result">
<h2>Rank: {r["rank"]}</h2>
<p><b>Document ID:</b> {html.escape(r["document_id"])}</p>
<p><b>Original Score:</b> {r["score"]}</p>
<p><b>Rerank Score:</b> {r.get("rerank_score","")}</p>
<p><b>Rerank Score:</b> {r.get("qwen_score","")}</p>

<h3>Content</h3>
<div class="content">{html.escape(r["content"])}</div>

<h3>Metadata</h3>
<div class="metadata">{metadata_html}</div>
</div>
""")

html_parts.append("</body></html>")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

print("HTML file written to:", output_file)
# usage: python script.py reranked_qwen8.json results_qwen8.html
