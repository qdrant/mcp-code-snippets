import importlib.metadata
import os
import tomllib
from typing import Any

from mcp_code_snippets.explore.detect_language import ProgrammingLanguage
from mcp_code_snippets.explore.extract_deps.base import DependencyParserBase


class PythonDependencyParser(DependencyParserBase):
    @classmethod
    def language(cls) -> ProgrammingLanguage:
        return ProgrammingLanguage.PYTHON

    @classmethod
    def parse_dependencies(cls, project_root: str) -> dict[str, str | None]:
        """
        Parse the dependencies from a pyproject.toml file.

        Args:
            pyproject_path (str): Path to the pyproject.toml file.

        Returns:
            list[str]: List of dependencies.
        """

        pyproject_path = os.path.join(project_root, "pyproject.toml")

        if not os.path.exists(pyproject_path):
            return {}

        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)
            return cls._parse_dependencies(pyproject)

    @classmethod
    def _parse_dependencies(
        cls, pyproject_content: dict[str, Any]
    ) -> dict[str, str | None]:
        """Parse dependencies from the pyproject.toml file and retrieve version via importlib.

        Args:
            pyproject_content (dict): Parsed pyproject.toml content.

        Returns:
            dict[str, str | None]: List of dependencies.
        """

        raw_dependencies = []
        raw_dependencies.extend(cls._parse_poetry_dependencies(pyproject_content))
        raw_dependencies.extend(cls._parse_pypa_spec_dependencies(pyproject_content))

        clean_dependencies = cls._clean_dependencies(raw_dependencies)
        dependencies = cls._assign_versions(clean_dependencies)
        return dependencies

    @staticmethod
    def _parse_region(content: dict[str, Any], region: str) -> list[str]:
        if "." in region:
            regions = region.split(".")
            for region in regions:
                content = content.get(region, {})
        else:
            content = content.get(region, {})
        dependencies = []
        if isinstance(content, list):
            for dependency in content:
                if "<" in dependency:
                    dependency = dependency.split("<")[0].strip()
                elif ">" in dependency:
                    dependency = dependency.split(">")[0].strip()
                elif "=" in dependency:
                    dependency = dependency.split("=")[0].strip()
                elif "^" in dependency:
                    dependency = dependency.split("^")[1].strip()
                dependencies.append(dependency)
        elif isinstance(content, dict):
            dependencies = list(content.keys())
        return dependencies

    @classmethod
    def _parse_poetry_dependencies(cls, pyproject_content: dict[str, Any]) -> list[str]:
        """
        Parse poetry dependencies from the pyproject.toml file.

        Args:
            pyproject_content (dict): Parsed pyproject.toml content.

        Returns:
            list[str]: List of poetry dependencies.
        """
        fields = ["tool.poetry.dependencies", "tool.poetry.dev-dependencies"]

        for group in (
            pyproject_content.get("tool", {}).get("poetry", {}).get("group", {})
        ):
            fields.append(f"tool.poetry.group.{group}.dependencies")
            fields.append(f"tool.poetry.group.{group}.dev-dependencies")

        dependencies = []
        for field in fields:
            dependencies.extend(cls._parse_region(pyproject_content, field))

        return dependencies

    @classmethod
    def _parse_pypa_spec_dependencies(
        cls, pyproject_content: dict[str, Any]
    ) -> list[str]:
        """
        Parse PyPA specification dependencies from the pyproject.toml file.

        Args:
            pyproject_content (dict): Parsed pyproject.toml content.

        Returns:
            list[str]: List of PEP 621 dependencies.
        """
        fields = [
            "project.dependencies",
            "project.optional-dependencies",
        ]

        dependencies = []
        for field in fields:
            dependencies.extend(cls._parse_region(pyproject_content, field))

        dependency_groups = pyproject_content.get("project", {}).get(
            "dependency-groups", {}
        )
        for group, deps in dependency_groups.items():
            dependencies.extend(deps)
        return dependencies

    @staticmethod
    def _clean_dependencies(dependencies: list[str]) -> list[str]:
        """
        Clean the dependencies by removing extras and not installed packages.

        Args:
            dependencies (list[str]): List of dependencies.

        Returns:
            list[str]: list of installed dependencies.
        """
        clean_dependencies = []
        for dependency in dependencies:
            if dependency == "python":
                continue

            if "[" in dependency:
                dependency = dependency.split("[")[0].strip()

            clean_dependencies.append(dependency)
        return clean_dependencies

    @staticmethod
    def _assign_versions(dependencies: list[str]) -> dict[str, str]:
        """Assign versions to the dependencies via importlib.metadata

        Args:
            dependencies (list[str]): List of dependencies.

        Returns:
            dict[str, str]: Dictionary of dependencies with package names as keys and versions as values.
        """
        versioned_dependencies = {}
        for dependency in dependencies:
            try:
                version = importlib.metadata.version(dependency)
                versioned_dependencies[dependency] = (
                    version  # todo: split version into tuple or dict
                )
            except importlib.metadata.PackageNotFoundError:
                versioned_dependencies[dependency] = None
        return versioned_dependencies
