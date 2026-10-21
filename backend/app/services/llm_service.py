import os
from typing import List, Dict, Any
from openai import OpenAI

# Render Dashboard ke Environment Variables se key padhega
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("GROQ_API_KEY")


class AIService:
    def __init__(self, default_coder_model: str = "meta-llama/llama-3.3-70b-instruct"):
        self.coder_model = default_coder_model
        # OpenRouter Client via standard OpenAI SDK
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY if OPENROUTER_API_KEY else "dummy_key"
        ) if OPENROUTER_API_KEY else None

    def _query_llm(self, prompt: str) -> str:
        """Queries LLM via OpenRouter with auto-fallback models."""
        if not self.client or not OPENROUTER_API_KEY:
            return "⚠️ Error: OPENROUTER_API_KEY environment variable is not set on Render dashboard."

        # Active production models on OpenRouter
        models_to_try = [
            self.coder_model,
            "meta-llama/llama-3.3-70b-instruct",
            "meta-llama/llama-3.1-8b-instruct",
            "mistralai/mistral-small-24b-instruct-2501"
        ]

        # Order preserve karke duplicates remove karte hain
        seen = set()
        unique_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

        for model_name in unique_models:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=4096
                )
                return response.choices[0].message.content
            except Exception as e:
                err_msg = str(e)
                if any(k in err_msg for k in ["404", "model_not_found", "decommissioned", "400"]):
                    continue
                return f"⚠️ Error calling OpenRouter API ({model_name}): {err_msg}"

        return "⚠️ Error: None of the configured OpenRouter models were available."

    def analyze_architecture(self, files_summary: List[Dict[str, Any]]) -> str:
        context_str = "".join([f"File: {f['path']} ({f['line_count']} lines)\n" for f in files_summary[:25]])
        prompt = (
            "You are an expert Software Architect and DevOps Engineer.\n"
            "Analyze the following repository structure:\n\n"
            f"{context_str}\n\n"
            "Provide:\n"
            "1. High-Level Architecture: Tech stack, pattern, key modules.\n"
            "2. Entry Point: Main execution point.\n"
            "3. Architecture Diagram: Generate valid Markdown Mermaid.js flowchart (inside ```mermaid codeblock).\n\n"
            "STRICT MERMAID SYNTAX RULES:\n"
            "- Start with `graph TD`\n"
            "- Use simple single-word Node IDs (e.g. `NodeA`, `NodeB`). No slashes or spaces.\n"
            "- Wrap node display text in double quotes inside brackets: `NodeA[\"GitHub Repo\"] --> NodeB[\"CI/CD\"]`\n"
        )
        return self._query_llm(prompt)

    def scan_repository_security(self, files: List[Dict[str, Any]]) -> str:
        code_files = [f for f in files if f['extension'] in ['.py', '.js', '.ts', '.java', '.go', '.php', '.rb', '.cpp', '.tf']]
        code_context = "".join([f"\n--- FILE: {f['path']} ---\n{f['content'][:1500]}\n" for f in code_files[:10]])
        prompt = (
            "You are a Lead Cybersecurity Auditor & SAST Expert.\n"
            "Perform an in-depth security and bug audit:\n\n"
            f"{code_context}\n\n"
            "Provide structured audit report with:\n"
            "1. Executive Security Summary & Health Score\n"
            "2. Vulnerabilities Identified (Severity, Path, Flaw)\n"
            "3. Remediation & Code Snippets\n"
            "4. DevOps Security Recommendations"
        )
        return self._query_llm(prompt)

    def generate_readme_docs(self, files: List[Dict[str, Any]]) -> str:
        file_tree = "\n".join([f"- {f['path']}" for f in files[:30]])
        snippets = "".join([f"\nFile: {f['path']}\n```{f['content'][:500]}\n```\n" for f in files[:5]])
        prompt = (
            "You are a Technical Writer. Generate production-ready `README.md` for this repository:\n\n"
            f"FILE STRUCTURE:\n{file_tree}\n\n"
            f"CODE SNIPPETS:\n{snippets}\n\n"
            "Output ONLY clean Markdown formatted text."
        )
        return self._query_llm(prompt)

    def recommend_cloud_optimization(self, files: List[Dict[str, Any]]) -> str:
        file_tree = "\n".join([f"- {f['path']}" for f in files[:30]])
        prompt = (
            "You are a Cloud Architect. Analyze file structure and recommend Cloud & Cost Strategy:\n\n"
            f"PROJECT FILES:\n{file_tree}\n\n"
            "1. Cloud Hosting Providers\n2. Optimal Architecture & Sizing\n3. Cost Optimization Checklist\n4. Caching & Scaling Strategy"
        )
        return self._query_llm(prompt)

    def generate_devops_manifests(self, files: List[Dict[str, Any]]) -> str:
        file_tree = "\n".join([f"- {f['path']}" for f in files[:30]])
        prompt = (
            "You are a DevOps Lead. Generate configurations:\n\n"
            f"PROJECT FILES:\n{file_tree}\n\n"
            "1. Dockerfile\n2. docker-compose.yml\n3. Kubernetes Manifests\n4. GitHub Actions CI/CD Pipeline"
        )
        return self._query_llm(prompt)