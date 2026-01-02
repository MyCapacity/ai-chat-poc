# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This file contains the tools used by the database agent."""
import os


class FileTool:
    def __init__(self, base_path: str, encoding: str = "utf-8"):
        self.base_path = os.path.abspath(base_path)
        self.encoding = encoding

    def _resolve_path(self, path: str) -> str:
        full_path = os.path.abspath(os.path.join(self.base_path, path))
        if not full_path.startswith(self.base_path):
            raise ValueError(f"Access denied: {path} is outside the base path")
        return full_path

    def read(self, filepath: str, create_if_missing: bool = False) -> str:
        path = self._resolve_path(filepath)
        if not os.path.exists(path):
            if create_if_missing:
                open(path, "w", encoding=self.encoding).close()
                return f"📁 File created at {path} (empty)"
            return f"❌ File not found: {path}"
        with open(path, "r", encoding=self.encoding) as f:
            return f"📖 Read from {path}:\n{f.read()}"

    def write(self, filepath: str, content: str, create_if_missing: bool = True) -> str:
        path = self._resolve_path(filepath)

        # If file doesn't exist and creation isn't allowed, return early
        if not os.path.exists(path) and not create_if_missing:
            return f"❌ File not found and 'create_if_missing' is False"

        # Ensure parent directory exists if creation is allowed
        parent_dir = os.path.dirname(path)
        if create_if_missing and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # Write content to file
        with open(path, "w", encoding=self.encoding) as f:
            f.write(content)

        return f"✅ Wrote to {path}"


    def list(self, directory: str) -> str:
        path = self._resolve_path(directory)
        if not os.path.isdir(path):
            return f"❌ {path} is not a directory"
        files = os.listdir(path)
        return f"📂 Contents of {path}:\n" + "\n".join(files)

    def check_permissions(self, path: str) -> str:
        resolved = self._resolve_path(path)
        perms = []
        if os.access(resolved, os.R_OK):
            perms.append("readable")
        if os.access(resolved, os.W_OK):
            perms.append("writable")
        if os.access(resolved, os.X_OK):
            perms.append("executable")
        return f"🔐 Permissions for {resolved}: {', '.join(perms)}" if perms else f"🚫 No permissions for {resolved}"

