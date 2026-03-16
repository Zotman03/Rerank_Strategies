import re, json

def parse_results(text):
    pattern = r"Result\s+(\d+):\nScore:\s*([\d.]+)\nDocument ID:\s*(.*?)\nContent:\n-+\n(.*?)\n-+\nMetadata:\s*(\{.*?\})"
    
    matches = re.findall(pattern, text, re.DOTALL)

    results = []
    
    for rank, score, doc_id, content, metadata in matches:
        results.append({
            "rank": int(rank),
            "score": float(score),
            "document_id": doc_id.strip(),
            "content": content.strip(),
            "metadata": json.loads(metadata)
        })
        
    return results


with open("slurm.out") as f:
    text = f.read()

parsed = parse_results(text)

with open("parsed_results.json", "w") as f:
    json.dump(parsed, f, indent=2)
