import json
from flashrank import Ranker, RerankRequest

with open("parsed_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

query = "By how much of the ocean surface warming occurred since 1980"
# ranker = Ranker() #MSmarco
ranker = Ranker(model_name="rank-T5-flan")
passages = [
    {
        "id": str(r["rank"]),
        "text": r["content"]
    }
    for r in results
]

rerank_request = RerankRequest(query=query, passages=passages)
reranked = ranker.rerank(rerank_request)
# https://github.com/PrithivirajDamodaran/FlashRank

reranked_results = []
for r in reranked:
    original = next(x for x in results if str(x["rank"]) == r["id"])
    original["rerank_score"] = float(r["score"])
    reranked_results.append(original)

reranked_results = sorted(reranked_results, key=lambda x: x["rerank_score"], reverse=True)

with open("reranked_results.json", "w", encoding="utf-8") as f:
    json.dump(reranked_results, f, indent=2, ensure_ascii=False)
