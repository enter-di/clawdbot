"""Tests for the GitHub tool definitions in the tool registry."""

import pytest

from openclaw.agent.tool_registry import TOOLS


def _get_tool(name: str) -> dict:
    return next((t for t in TOOLS if t["name"] == name), None)


class TestCreateGithubIssueTool:
    def test_tool_exists(self):
        assert _get_tool("create_github_issue") is not None

    def test_required_fields(self):
        tool = _get_tool("create_github_issue")
        required = tool["input_schema"]["required"]
        assert "owner" in required
        assert "repo" in required
        assert "title" in required

    def test_optional_fields_present(self):
        tool = _get_tool("create_github_issue")
        props = tool["input_schema"]["properties"]
        assert "body" in props
        assert "labels" in props
        assert "assignees" in props

    def test_labels_is_array_of_strings(self):
        tool = _get_tool("create_github_issue")
        labels_schema = tool["input_schema"]["properties"]["labels"]
        assert labels_schema["type"] == "array"
        assert labels_schema["items"]["type"] == "string"

    def test_assignees_is_array_of_strings(self):
        tool = _get_tool("create_github_issue")
        assignees_schema = tool["input_schema"]["properties"]["assignees"]
        assert assignees_schema["type"] == "array"
        assert assignees_schema["items"]["type"] == "string"


class TestSearchGithubTool:
    def test_tool_exists(self):
        assert _get_tool("search_github") is not None

    def test_query_is_required(self):
        tool = _get_tool("search_github")
        assert "query" in tool["input_schema"]["required"]

    def test_type_enum_values(self):
        tool = _get_tool("search_github")
        type_schema = tool["input_schema"]["properties"]["type"]
        assert set(type_schema["enum"]) == {"repositories", "issues", "users", "code"}

    def test_max_results_has_default(self):
        tool = _get_tool("search_github")
        max_results = tool["input_schema"]["properties"]["max_results"]
        assert max_results["default"] == 5

    def test_type_defaults_to_repositories(self):
        tool = _get_tool("search_github")
        type_schema = tool["input_schema"]["properties"]["type"]
        assert type_schema["default"] == "repositories"


def test_github_tools_pass_schema_validation():
    """Ensure both new tools satisfy the generic schema requirements."""
    for name in ("create_github_issue", "search_github"):
        tool = _get_tool(name)
        assert tool is not None, f"Tool '{name}' missing"
        assert "name" in tool
        assert "description" in tool
        assert "input_schema" in tool
        assert tool["input_schema"]["type"] == "object"
        assert "properties" in tool["input_schema"]
