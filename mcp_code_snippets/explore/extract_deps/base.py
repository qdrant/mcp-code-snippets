from mcp_code_snippets.explore.detect_language import ProgrammingLanguage


class DependencyParserBase:
    @classmethod
    def language(cls) -> ProgrammingLanguage:
        """
        Return the language of the project.
        """
        raise NotImplementedError("Not implemented")

    @classmethod
    def parse_dependencies(cls, _project_root: str) -> dict[str, str | None]:
        """
        Parse the dependencies from the project root.
        """
        raise NotImplementedError("Not implemented")
