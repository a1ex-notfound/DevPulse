import ollama
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CodebaseRAGService:
    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        self.model_name = model_name

    def _chunk_code_files(self, files: List[Dict[str, Any]], max_chunk_lines: int = 45) -> List[Dict[str, Any]]:
        """Splits source files into manageable code chunks for vector search."""
        chunks = []
        for file_obj in files:
            lines = file_obj['content'].splitlines()
            if not lines:
                continue

            for i in range(0, len(lines), max_chunk_lines):
                chunk_lines = lines[i:i + max_chunk_lines]
                chunk_text = "\n".join(chunk_lines)
                chunks.append({
                    "file_path": file_obj["path"],
                    "start_line": i + 1,
                    "end_line": i + len(chunk_lines),
                    "content": chunk_text
                })
        return chunks

    def answer_question(self, files: List[Dict[str, Any]], question: str) -> str:
        """Finds most relevant code chunks and generates an AI answer."""
        chunks = self._chunk_code_files(files)
        if not chunks:
            return "No readable code files found in the repository to answer your question."

        corpus = [f"{c['file_path']}\n{c['content']}" for c in chunks]

        # RAG Retrieval via TF-IDF & Cosine Similarity
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(corpus)
            question_vector = vectorizer.transform([question])
            
            similarities = cosine_similarity(question_vector, tfidf_matrix).flatten()
            top_indices = similarities.argsort()[-4:][::-1]  # Get top 4 most relevant chunks
        except Exception:
            top_indices = list(range(min(4, len(chunks))))

        context_str = ""
        for idx in top_indices:
            chunk = chunks[idx]
            context_str += f"\n--- FILE: {chunk['file_path']} (Lines {chunk['start_line']}-{chunk['end_line']}) ---\n"
            context_str += chunk['content'] + "\n"

        prompt = (
            "You are an expert Lead Developer AI Assistant.\n"
            "Use the following retrieved code snippets from the repository to answer the user's question.\n\n"
            f"RELEVANT CODE snippets:\n{context_str}\n\n"
            f"USER QUESTION: {question}\n\n"
            "Answer clearly and concisely. Mention exact file paths and line numbers wherever relevant."
        )

        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']