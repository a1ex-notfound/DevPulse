import os
import shutil
import tempfile
from typing import List, Dict, Any
from git import Repo

# Allowed code file extensions
ALLOWED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.cpp', '.c',
    '.rs', '.php', '.rb', '.html', '.css', '.json', '.yaml', '.yml',
    '.md', '.dockerfile', 'Dockerfile', '.sh', '.tf'
}

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', '.next', 'dist', 'build'}

class RepoIngestor:
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.temp_dir = None

    def clone_repository(self) -> str:
        """Clones the repository into a temporary directory."""
        self.temp_dir = tempfile.mkdtemp(prefix="devops_ai_")
        try:
            # Shallow clone (depth=1) for faster download
            Repo.clone_from(self.repo_url, self.temp_dir, depth=1)
            return self.temp_dir
        except Exception as e:
            self.cleanup()
            raise RuntimeError(f"Failed to clone repository: {str(e)}")

    def extract_code_files(self) -> List[Dict[str, Any]]:
        """Parses the cloned repository and extracts text code files."""
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise FileNotFoundError("Repository has not been cloned yet.")

        parsed_files = []

        for root, dirs, files in os.walk(self.temp_dir):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                filename = os.path.basename(file)

                if ext in ALLOWED_EXTENSIONS or filename in ALLOWED_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, self.temp_dir)

                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                        parsed_files.append({
                            "path": relative_path,
                            "file_name": file,
                            "extension": ext or filename,
                            "content": content,
                            "line_count": len(content.splitlines())
                        })
                    except Exception as e:
                        print(f"Skipping file {relative_path} due to read error: {e}")

        return parsed_files

    def cleanup(self):
        """Deletes temporary files after processing."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)