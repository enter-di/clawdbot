"""Validate tool registry schema."""

from openclaw.agent.tool_registry import TOOLS


def test_all_tools_have_required_keys():
    for tool in TOOLS:
        assert "name" in tool
        assert "description" in tool
        assert "input_schema" in tool
        schema = tool["input_schema"]
        assert schema["type"] == "object"
        assert "properties" in schema


def test_tool_names_are_unique():
    names = [t["name"] for t in TOOLS]
    assert len(names) == len(set(names))


def test_required_fields_exist_in_schema():
    for tool in TOOLS:
        if "required" in tool["input_schema"]:
            for req in tool["input_schema"]["required"]:
                assert req in tool["input_schema"]["properties"], (
                    f"Tool '{tool['name']}': required field '{req}' not in properties"
                )
