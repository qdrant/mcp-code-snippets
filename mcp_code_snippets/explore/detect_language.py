"""
This file contains helper tools to detect which programming language is used in the current codebase.
It expectes to receive a path to project root and then use a bunch of heuristics to detect the language.

For exaple, if the project root contains a file called "pyproject.toml", it's a python project.

"""

from enum import Enum
from typing import Optional
import os
import glob


class ProgrammingLanguage(Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    RUST = "rust"
    GOLANG = "golang"
    CSHARP = "csharp"


def detect_python_language(project_root: str) -> Optional[ProgrammingLanguage]:
    """
    Detect if the project is a Python project by looking for common Python project files.
    """
    python_indicators = [
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "setup.cfg",
        "Pipfile",
        "Pipfile.lock",
        "poetry.lock",
        "uv.lock",
        "*.py",
        ".venv",
        "venv",
        ".python-version",
    ]

    for indicator in python_indicators:
        if os.path.exists(os.path.join(project_root, indicator)):
            return ProgrammingLanguage.PYTHON
        if indicator.endswith("*.py"):
            if glob.glob(os.path.join(project_root, "**/*.py")):
                return ProgrammingLanguage.PYTHON
    return None


def detect_java_language(project_root: str) -> Optional[ProgrammingLanguage]:
    """
    Detect if the project is a Java project by looking for common Java project files.
    """
    java_indicators = [
        "pom.xml",  # Maven
        "build.gradle",  # Gradle
        "*.java",
        "*.class",
        "*.jar",
    ]

    for indicator in java_indicators:
        if os.path.exists(os.path.join(project_root, indicator)):
            return ProgrammingLanguage.JAVA
        if indicator.startswith("*."):
            if glob.glob(os.path.join(project_root, f"**/{indicator}")):
                return ProgrammingLanguage.JAVA
    return None


def detect_javascript_language(project_root: str) -> Optional[ProgrammingLanguage]:
    """
    Detect if the project is a JavaScript/Node.js project by looking for common files.
    """
    js_indicators = [
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "*.js",
        "*.jsx",
        "*.ts",
        "*.tsx",
    ]

    for indicator in js_indicators:
        if os.path.exists(os.path.join(project_root, indicator)):
            return ProgrammingLanguage.JAVASCRIPT
        if indicator.startswith("*."):
            if glob.glob(os.path.join(project_root, f"**/{indicator}")):
                return ProgrammingLanguage.JAVASCRIPT
    return None


def detect_rust_language(project_root: str) -> Optional[ProgrammingLanguage]:
    """
    Detect if the project is a Rust project by looking for common Rust project files.
    """
    rust_indicators = ["Cargo.toml", "Cargo.lock", "*.rs"]

    for indicator in rust_indicators:
        if os.path.exists(os.path.join(project_root, indicator)):
            return ProgrammingLanguage.RUST
        if indicator.startswith("*."):
            if glob.glob(os.path.join(project_root, f"**/{indicator}")):
                return ProgrammingLanguage.RUST
    return None


def detect_golang_language(project_root: str) -> Optional[ProgrammingLanguage]:
    """
    Detect if the project is a Go project by looking for common Go project files.
    """
    go_indicators = ["go.mod", "go.sum", "*.go"]

    for indicator in go_indicators:
        if os.path.exists(os.path.join(project_root, indicator)):
            return ProgrammingLanguage.GOLANG
        if indicator.startswith("*."):
            if glob.glob(os.path.join(project_root, f"**/{indicator}")):
                return ProgrammingLanguage.GOLANG
    return None


def detect_csharp_language(project_root: str) -> Optional[ProgrammingLanguage]:
    """
    Detect if the project is a C# project by looking for common C# project files.
    """
    csharp_indicators = ["*.csproj", "*.sln", "*.cs"]

    for indicator in csharp_indicators:
        if os.path.exists(os.path.join(project_root, indicator)):
            return ProgrammingLanguage.CSHARP
        if indicator.startswith("*."):
            if glob.glob(os.path.join(project_root, f"**/{indicator}")):
                return ProgrammingLanguage.CSHARP
    return None


def detect_language(project_root: str) -> Optional[ProgrammingLanguage]:
    """
    Detect the programming language used in the current codebase.
    """
    if detect_python_language(project_root):
        return ProgrammingLanguage.PYTHON
    elif detect_java_language(project_root):
        return ProgrammingLanguage.JAVA
    elif detect_javascript_language(project_root):
        return ProgrammingLanguage.JAVASCRIPT
    elif detect_rust_language(project_root):
        return ProgrammingLanguage.RUST
    elif detect_golang_language(project_root):
        return ProgrammingLanguage.GOLANG
    elif detect_csharp_language(project_root):
        return ProgrammingLanguage.CSHARP
    else:
        return None
