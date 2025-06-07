from mcp_code_snippets.explore.detect_language import ProgrammingLanguage
from mcp_code_snippets.explore.extract_deps.base import DependencyParserBase


class JavaDependencyParser(DependencyParserBase):
    @classmethod
    def language(cls) -> ProgrammingLanguage:
        return ProgrammingLanguage.JAVA

    @classmethod
    def parse_dependencies(cls, _project_root: str) -> dict[str, str | None]:
        """
        Parse the dependencies from a pom.xml file.
        """

        # TODO: This method is not implemented yet.
        return {}
