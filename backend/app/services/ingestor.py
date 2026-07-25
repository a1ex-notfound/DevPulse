import os
import shutil
import tempfile
from typing import List, Dict, Any
from git import Repo


class RepositoryIngestor:
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.temp_dir = tempfile.mkdtemp()
        self.files_data = []

    def process_repository(self) -> List[Dict[str, Any]]:
        """Clones the repository and extracts file contents."""
        try:
            # Shallow clone for speed
            Repo.clone_from(self.repo_url, self.temp_dir, depth=1)

            ignored_extensions = {
                '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip',
                '.tar', '.gz', '.exe', '.pyc', '.git', '.mp4', '.mp3', '.ttf'
            }
            ignored_dirs = {
                '.git', '__pycache__', 'node_modules', 'venv', '.venv',
                'build', 'dist', '.idea', '.vscode'
            }

            for root, dirs, files in os.walk(self.temp_dir):
                dirs[:] = [d for d in dirs if d not in ignored_dirs]

                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in ignored_extensions:
                        continue

                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.temp_dir)

                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            line_count = len(content.splitlines())

                            self.files_data.append({
                                "path": rel_path,
                                "content": content,
                                "line_count": line_count,
                                "extension": ext
                            })
                    except Exception:
                        continue

            return self.files_data
        finally:
            # Cleanup temp directory when finished
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def get_summary(self) -> List[Dict[str, Any]]:
        """Returns summary metadata of processed files."""
        return [
            {
                "path": f["path"],
                "line_count": f["line_count"],
                "extension": f["extension"]
            }
            for f in self.files_data
        ]