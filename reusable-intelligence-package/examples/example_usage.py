"""
Example: Using the MCP Tool Generator from the Reusable Intelligence Package
"""

# This is a conceptual example showing how to use the MCP Tool Generator
# In practice, you would have the actual implementation files

def example_mcp_tool_usage():
    """
    Demonstrates how to use the MCP Tool Generator to create a custom tool
    """
    print("Example: Creating a custom task management MCP tool")

    # Import the MCP Tool Generator from the package
    # from reusable_intelligence_package.agent_skills.mcp_tool_generator.skill import MCPTollGenerator

    # Define the tool specification
    tool_spec = {
        "name": "create_project_task",
        "description": "Create a new task in the project management system",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the task",
                    "minLength": 1,
                    "maxLength": 200
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the task",
                    "maxLength": 1000
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Priority level of the task"
                },
                "assignee": {
                    "type": "string",
                    "description": "User ID of the person assigned to the task"
                }
            },
            "required": ["title", "assignee"]
        }
    }

    # Generate the tool (conceptual)
    print("Tool specification:")
    print(f"  Name: {tool_spec['name']}")
    print(f"  Description: {tool_spec['description']}")
    print(f"  Properties: {list(tool_spec['input_schema']['properties'].keys())}")

    print("\nGenerated MCP tool ready for integration!")
    print("This tool includes:")
    print("- Input validation based on JSON schema")
    print("- Error handling for invalid inputs")
    print("- User data isolation patterns")
    print("- Proper response formatting")


def example_sub_agent_usage():
    """
    Demonstrates how to use a sub-agent template to create a custom agent
    """
    print("\nExample: Creating a custom analytics agent from template")

    # Conceptual example of extending a sub-agent template
    print("Extending the TEMPLATE sub-agent to create AnalyticsAgent:")
    print("- Inherits base agent functionality")
    print("- Adds custom analytics processing logic")
    print("- Maintains consistent interface patterns")
    print("- Preserves error handling and validation")


if __name__ == "__main__":
    print("Reusable Intelligence Package - Usage Examples")
    print("=" * 50)

    example_mcp_tool_usage()
    example_sub_agent_usage()

    print("\nTo use these components in your project:")
    print("1. Copy the desired components from the package")
    print("2. Customize the configuration for your use case")
    print("3. Integrate with your existing application")
    print("4. Test thoroughly before deployment")