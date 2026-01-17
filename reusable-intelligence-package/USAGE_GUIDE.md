# Usage Guide

## Introduction

This guide provides step-by-step instructions on how to effectively use the Reusable Intelligence Package in your projects. Following these steps will help you leverage the pre-built components efficiently while maintaining best practices.

## Step-by-Step Guide to Reuse Skills

### Step 1: Assess Your Project Needs
1. Identify the types of AI interactions your project requires
2. Match your needs to the available agent skills and sub-agents
3. Determine which components are most relevant to your use case

### Step 2: Set Up Your Project Environment
1. Ensure your project meets the prerequisites:
   - Python 3.8+
   - Compatible AI framework (OpenAI, Anthropic, etc.)
   - Required dependencies

2. Create a directory structure that accommodates the components:
   ```
   your-project/
   ├── agents/
   ├── skills/
   ├── tools/
   └── config/
   ```

### Step 3: Integrate Agent Skills
1. Copy the desired agent skill directories to your project:
   ```bash
   cp -r reusable-intelligence-package/agent-skills/mcp-tool-generator your-project/skills/
   ```

2. Import and configure the skill in your application:
   ```python
   from skills.mcp_tool_generator.skill import MCPTollGenerator

   generator = MCPTollGenerator(config)
   tool = generator.create_tool(tool_specification)
   ```

### Step 4: Integrate Sub-Agents
1. Copy the relevant sub-agent directories:
   ```bash
   cp -r reusable-intelligence-package/sub-agents/task-manager your-project/agents/
   ```

2. Configure and instantiate the sub-agent:
   ```python
   from agents.task_manager import TaskManagementAgent

   task_agent = TaskManagementAgent(
       api_key=os.getenv("OPENAI_API_KEY"),
       model="gpt-4"
   )
   ```

### Step 5: Customize Configuration
1. Adapt configuration files to your project:
   - Update API endpoints
   - Modify business logic rules
   - Adjust validation parameters

2. Test the integration thoroughly before deployment

## Example: Using MCP Tool Generator in New Project

### Scenario
You need to create an MCP tool for managing user profiles in your application.

### Steps

1. **Import the Generator**
   ```python
   from reusable_intelligence_package.agent_skills.mcp_tool_generator.skill import MCPTollGenerator
   ```

2. **Define Your Tool Specification**
   ```python
   user_profile_tool_spec = {
       "name": "manage_user_profile",
       "description": "Manage user profile information including preferences and settings",
       "input_schema": {
           "type": "object",
           "properties": {
               "user_id": {"type": "string", "description": "Unique identifier of the user"},
               "action": {"type": "string", "enum": ["get", "update", "delete"]},
               "profile_data": {
                   "type": "object",
                   "properties": {
                       "email": {"type": "string", "format": "email"},
                       "preferences": {"type": "object"}
                   }
               }
           },
           "required": ["user_id", "action"]
       }
   }
   ```

3. **Generate the Tool**
   ```python
   generator = MCPTollGenerator()
   user_profile_tool = generator.create_tool(user_profile_tool_spec)
   ```

4. **Integrate with Your Agent**
   ```python
   agent.tools.append(user_profile_tool)
   ```

5. **Test the Integration**
   ```python
   # Test with a sample request
   response = agent.process({
       "user_id": "user123",
       "action": "update",
       "profile_data": {
           "email": "newemail@example.com"
       }
   })
   ```

## Example: Creating New Sub-Agent from Template

### Scenario
You need to create a customer support agent for your e-commerce application.

### Steps

1. **Start with the Template**
   ```bash
   cp -r reusable-intelligence-package/sub-agents/TEMPLATE your-project/agents/customer_support
   ```

2. **Customize the Agent Class**
   ```python
   # agents/customer_support/customer_support_agent.py
   from sub_agents.TEMPLATE.agent_template import BaseAgent

   class CustomerSupportAgent(BaseAgent):
       def __init__(self):
           super().__init__(
               name="customer_support_agent",
               description="Handles customer inquiries and support tickets",
               model="gpt-4"
           )
           self.knowledge_base = self.load_knowledge_base()

       def process_request(self, user_input, context):
           # Implement customer support logic
           intent = self.classify_intent(user_input)

           if intent == "product_inquiry":
               return self.handle_product_inquiry(user_input, context)
           elif intent == "return_request":
               return self.handle_return_request(user_input, context)
           else:
               return self.handle_general_inquiry(user_input, context)
   ```

3. **Implement Specific Functions**
   ```python
   def classify_intent(self, user_input):
       # Use NLP to classify the user's intent
       # Return "product_inquiry", "return_request", etc.
       pass

   def handle_product_inquiry(self, user_input, context):
       # Handle product-related questions
       product_info = self.search_products(user_input)
       return self.format_response(product_info)
   ```

4. **Configure and Register the Agent**
   ```python
   # config/agents.py
   from agents.customer_support.customer_support_agent import CustomerSupportAgent

   CUSTOMER_SUPPORT_AGENT = CustomerSupportAgent()

   # Register with orchestrator
   orchestrator.register_agent(CUSTOMER_SUPPORT_AGENT)
   ```

5. **Test the New Agent**
   ```python
   # test_customer_support.py
   import pytest
   from agents.customer_support.customer_support_agent import CustomerSupportAgent

   def test_product_inquiry():
       agent = CustomerSupportAgent()
       response = agent.process_request(
           "What are the features of product XYZ?",
           {}
       )
       assert "features" in response.lower()
   ```

## Best Practices

### 1. Maintain Separation of Concerns
- Keep core reusable components separate from project-specific customizations
- Use inheritance or composition rather than modifying base components

### 2. Configuration Over Code
- Use configuration files for environment-specific settings
- Avoid hardcoding values that may vary between deployments

### 3. Consistent Naming Conventions
- Follow the naming patterns established in the reusable components
- Use descriptive names that clearly indicate functionality

### 4. Comprehensive Testing
- Adapt existing tests for your specific use cases
- Add tests for customizations and integrations
- Use the same testing frameworks and patterns

### 5. Documentation Updates
- Update documentation to reflect your customizations
- Maintain the same documentation standards
- Include examples specific to your implementation

### 6. Version Management
- Track versions of the reusable components you're using
- Plan for updates and compatibility maintenance
- Document any breaking changes in your adaptations

### 7. Error Handling Consistency
- Maintain consistent error handling patterns
- Use the same error codes and message formats
- Preserve the robustness of the original components

### 8. Performance Monitoring
- Implement monitoring for the reused components
- Track usage patterns and performance metrics
- Plan for scaling based on actual usage

## Troubleshooting

### Common Issues and Solutions

1. **Import Errors**
   - Ensure the package directory structure is preserved
   - Check Python path and module resolution
   - Verify all dependencies are installed

2. **Configuration Problems**
   - Review configuration file formats
   - Ensure all required parameters are provided
   - Check environment variable settings

3. **Integration Failures**
   - Verify API compatibility
   - Check data format expectations
   - Review error logs for specific issues

4. **Performance Issues**
   - Monitor resource usage
   - Review implementation for inefficiencies
   - Consider caching strategies for repeated operations

## Advanced Usage

### Extending Components
- Use inheritance to extend functionality while preserving interfaces
- Implement additional methods without changing core behavior
- Follow the open/closed principle (open for extension, closed for modification)

### Composing Multiple Components
- Combine multiple agent skills for complex behaviors
- Chain sub-agents for multi-step processes
- Use orchestrators to manage component interactions

### Customization Patterns
- Use factory patterns for dynamic component creation
- Implement adapter patterns for interface compatibility
- Apply decorator patterns for cross-cutting concerns

This usage guide provides a foundation for effectively leveraging the Reusable Intelligence Package in your projects. Remember to adapt these patterns to your specific requirements while maintaining the benefits of reusability and consistency.