import os
from typing import List, Dict, Any
from groq import Groq

# Environment Variable se API Key padhega (100% Safe)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class AIService:
    def __init__(self, default_coder_model: str = "llama-3.3-70b-versatile"):
        self.coder_model = default_coder_model
        # Groq client initialize tabhi hoga jab key present hogi
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

    def _query_llm(self, prompt: str) -> str:
        """Internal helper method to call Groq API reliably."""
        if not self.client:
            return "⚠️ Error: GROQ_API_KEY environment variable is not set. Please set it in your .env or environment."

        try:
            response = self.client.chat.completions.create(
                model=self.coder_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error calling Groq API: {str(e)}"

    def analyze_architecture(self, files_summary: List[Dict[str, Any]]) -> str:
        """Generates project architecture breakdown and Mermaid.js diagram."""
        context_str = ""
        for f in files_summary[:25]:
            context_str += f"File: {f['path']} ({f['line_count']} lines)\n"

        prompt = (
            "You are an expert Software Architect and DevOps Engineer.\n"
            "Analyze the following repository structure:\n\n"
            f"{context_str}\n\n"
            "Provide:\n"
            "1. High-Level Architecture: Overall tech stack, pattern (MVC, Microservices, Monolith, etc.), and key modules.\n"
            "2. Entry Point: Main execution point of the app.\n"
            "3. Architecture Diagram: Generate a valid Markdown Mermaid.js flowchart (inside ```mermaid codeblock).\n\n"
            "STRICT MERMAID SYNTAX RULES:\n"
            "- Start with `graph TD`\n"
            "- Use simple single-word Node IDs (e.g. `NodeA`, `NodeB`, `Repo`, `Server`). NEVER use slashes, hyphens, or spaces in Node IDs.\n"
            "- ALWAYS wrap node display text in double quotes inside brackets. Example: `NodeA[\"GitHub Repository\"] --> NodeB[\"CI/CD Server\"]`\n"
            "- Keep diagram clean, minimal (6-10 key nodes), and strictly valid.\n"
        )

        return self._query_llm(prompt)

    def scan_repository_security(self, files: List[Dict[str, Any]]) -> str:
        """Scans codebase files for OWASP Top 10 vulnerabilities, hardcoded credentials, and code smells."""
        code_files = [
            f for f in files 
            if f['extension'] in ['.py', '.js', '.ts', '.java', '.go', '.php', '.rb', '.cpp', '.tf']
        ]
        
        code_context = ""
        for f in code_files[:10]:
            snippet = f['content'][:1500]
            code_context += f"\n--- FILE: {f['path']} ---\n{snippet}\n"

        prompt = (
            "You are a Lead Cybersecurity Auditor & Static Application Security Testing (SAST) Expert.\n"
            "Perform an in-depth security and bug audit on the following codebase snippet:\n\n"
            f"{code_context}\n\n"
            "Provide a structured audit report with:\n"
            "1. Executive Security Summary: Overall security health score (e.g., A/B/C/D/F) and key risk areas.\n"
            "2. Vulnerabilities & Bugs Identified:\n"
            "   - Vulnerability/Bug Name & Risk Level (CRITICAL, HIGH, MEDIUM, LOW)\n"
            "   - Affected File Path\n"
            "   - Flaw Explanation\n"
            "3. Remediation & Secure Refactoring: Show corrected/safe code snippets for the key issues.\n"
            "4. DevOps Security Recommendations: Suggestions for CI/CD secret scanning, dependency updates, and SAST tools.\n"
        )

        return self._query_llm(prompt)

    def generate_readme_docs(self, files: List[Dict[str, Any]]) -> str:
        """Generates a comprehensive professional README.md for the repository."""
        file_tree = "\n".join([f"- {f['path']}" for f in files[:30]])
        
        snippets = ""
        for f in files[:5]:
            snippets += f"\nFile: {f['path']}\n```{f['content'][:500]}\n```\n"

        prompt = (
            "You are a Technical Writer and Senior Developer.\n"
            "Generate an exhaustive, professional, production-ready `README.md` for this repository.\n\n"
            f"FILE STRUCTURE:\n{file_tree}\n\n"
            f"CODE SNIPPETS:\n{snippets}\n\n"
            "The README.md MUST include:\n"
            "1. Project Title & Catchy Description\n"
            "2. Tech Stack Badges/List\n"
            "3. Key Features\n"
            "4. Project Directory Structure\n"
            "5. Step-by-Step Installation & Local Setup Instructions\n"
            "6. Environment Variables (if applicable)\n"
            "7. How to Run / Usage Examples\n"
            "8. Contributing Guidelines & License Section\n\n"
            "Output ONLY clean Markdown formatted text."
        )

        return self._query_llm(prompt)

    def recommend_cloud_optimization(self, files: List[Dict[str, Any]]) -> str:
        """Recommends cloud deployment strategy and cost optimization plan."""
        file_tree = "\n".join([f"- {f['path']}" for f in files[:30]])

        prompt = (
            "You are a Principal Cloud Solutions Architect and DevOps Cost Optimization Consultant.\n"
            "Analyze this codebase file structure and recommend a Cloud Deployment & Cost Saving Strategy:\n\n"
            f"PROJECT FILES:\n{file_tree}\n\n"
            "Provide:\n"
            "1. **Recommended Cloud Hosting Providers**: (e.g., AWS, Vercel, GCP, DigitalOcean) with reasoning.\n"
            "2. **Optimal Architecture & Sizing**: (Serverless Lambda vs Docker ECS/EKS vs VM) + Recommended vCPU/RAM specs.\n"
            "3. **Cost Optimization & Reduction Checklist**: Top 5 actionable rules to reduce monthly infrastructure bills.\n"
            "4. **Caching & Scaling Strategy**: CDN setup, Redis caching, auto-scaling thresholds.\n"
        )

        return self._query_llm(prompt)

    def generate_devops_manifests(self, files: List[Dict[str, Any]]) -> str:
        """Generates production-grade Dockerfile, docker-compose.yml, K8s manifests, and GitHub Actions CI/CD."""
        file_tree = "\n".join([f"- {f['path']}" for f in files[:30]])

        prompt = (
            "You are an expert DevOps Lead Engineer.\n"
            "Based on the project files below, generate complete, production-ready DevOps configurations:\n\n"
            f"PROJECT FILES:\n{file_tree}\n\n"
            "Generate four distinct sections with clean code blocks:\n"
            "1. **Dockerfile**: Multi-stage build Dockerfile tailored for this tech stack.\n"
            "2. **docker-compose.yml**: Multi-container docker-compose setup including the application and database/redis services.\n"
            "3. **Kubernetes Deployment Manifest (`deployment.yaml`)**: K8s Deployment, ClusterIP Service, and HorizontalPodAutoscaler.\n"
            "4. **GitHub Actions CI/CD Pipeline (`.github/workflows/ci.yml`)**: Workflow for Linting, Security SAST Scan, Docker Build, and Push.\n"
        )

        return self._query_llm(prompt)