from typing import List, Dict, Any


class CodebaseRAG:
    def __init__(self):
        self.files = []

    def index_repository(self, files: List[Dict[str, Any]]):
        """Indexes the processed codebase files."""
        self.files = files

    def query(self, user_query: str, ai_service: Any) -> str:
        """Finds relevant file snippets and queries the LLM."""
        if not self.files:
            return "No repository files indexed yet."

        query_terms = user_query.lower().split()
        matched_files = []

        for f in self.files:
            score = sum(1 for term in query_terms if term in f["content"].lower() or term in f["path"].lower())
            if score > 0:
                matched_files.append((score, f))

        matched_files.sort(key=lambda x: x[0], reverse=True)
        top_matches = matched_files[:5]

        relevant_snippets = ""
        if top_matches:
            for _, f in top_matches:
                relevant_snippets += f"\n--- FILE: {f['path']} ---\n{f['content'][:1000]}\n"
        else:
            for f in self.files[:3]:
                relevant_snippets += f"\n--- FILE: {f['path']} ---\n{f['content'][:1000]}\n"

        prompt = (
            f"Codebase Context Snippets:\n{relevant_snippets}\n\n"
            f"User Question: {user_query}\n\n"
            "Answer the question clearly based on the provided codebase context."
        )

        return ai_service._query_llm(prompt)