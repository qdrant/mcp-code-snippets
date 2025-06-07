from typing import Optional
from mcp_code_snippets.explore.detect_language import ProgrammingLanguage
from mcp_code_snippets.explore.extract_deps.base import DependencyParserBase
from mcp_code_snippets.explore.extract_deps.csharp import CsharpDependencyParser
from mcp_code_snippets.explore.extract_deps.golang import GolangDependencyParser
from mcp_code_snippets.explore.extract_deps.java import JavaDependencyParser
from mcp_code_snippets.explore.extract_deps.python import PythonDependencyParser
from mcp_code_snippets.explore.extract_deps.rust import RustDependencyParser
from mcp_code_snippets.explore.extract_deps.typescript import TypescriptDependencyParser


DEPENDENCY_PARSERS = {
    ProgrammingLanguage.PYTHON: PythonDependencyParser,
    ProgrammingLanguage.JAVA: JavaDependencyParser,
    ProgrammingLanguage.JAVASCRIPT: TypescriptDependencyParser,
    ProgrammingLanguage.RUST: RustDependencyParser,
    ProgrammingLanguage.GOLANG: GolangDependencyParser,
    ProgrammingLanguage.CSHARP: CsharpDependencyParser,
}


# This is a fallback for the case when the language is not detected or
# if it was not possible to extract the dependencies.
DEFAULT_DEPENDENCIES = {"qdrant-client": None}


def get_dependencies(
    language: Optional[ProgrammingLanguage], project_root: str
) -> dict[str, str | None]:
    """
    Get the dependencies for a given language.
    """

    if language is None:
        return DEFAULT_DEPENDENCIES

    language_parser = DEPENDENCY_PARSERS.get(language)

    if language_parser is None:
        return DEFAULT_DEPENDENCIES

    dependencies = language_parser.parse_dependencies(project_root)

    if dependencies is None or len(dependencies) == 0:
        return DEFAULT_DEPENDENCIES

    return dependencies
