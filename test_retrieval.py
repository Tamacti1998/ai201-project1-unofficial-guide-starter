"""
Manual retrieval sanity check against the Evaluation Plan queries (planning.md).

For each query, prints the top-k chunks with their cosine DISTANCE scores
(0.0 = identical, higher = less related) so we can eyeball:
    "Are these chunks actually relevant to the question?"

Run: python test_retrieval.py
"""

from retriever import retrieve

# A subset (>=3) of the 5 Evaluation Plan queries from planning.md
EVAL_QUERIES = [
    "What specific reasons do students mention for finding organic chemistry difficult?",
    "What study strategies do successful students recommend to improve performance in organic chemistry?",
    "Based on student discussions, what determines how hard organic chemistry feels: the course itself or the instructor?",
]


def main():
    for qi, query in enumerate(EVAL_QUERIES, 1):
        print("=" * 90)
        print(f"QUERY {qi}: {query}")
        print("=" * 90)

        hits = retrieve(query)
        for i, hit in enumerate(hits, 1):
            distance = round(1 - hit["similarity"], 4)  # retriever stores similarity = 1 - distance
            print(f"\n  [{i}] distance={distance:.4f}  (similarity={hit['similarity']:.4f})")
            print(f"      source: {hit['doc_name']}  | chunk #{hit['chunk_index']}  | {hit['source_type']}")
            print(f"      title : {hit['title']}")
            print(f"      text  : {hit['text'][:220].strip()}...")
        print()


if __name__ == "__main__":
    main()
