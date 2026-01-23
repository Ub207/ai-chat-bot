# Sub-Agent Template

## 1. Agent Definition

### Name:
[Provide a descriptive name for the agent that reflects its primary function]

### Role:
[Define the agent's primary responsibility and purpose within the system]

### Triggers:
[List the conditions or events that activate this agent]
- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

### Capabilities:
[Describe the specific tasks and functions the agent can perform]
- Capability 1
- Capability 2
- Capability 3

## 2. System Instructions

### Personality:
[Define the agent's communication style and character traits]
- Trait 1
- Trait 2
- Trait 3

### Rules:
[Specify the operational guidelines and constraints for the agent]
- Rule 1
- Rule 2
- Rule 3
- Rule 4

### Behavior:
[Detail how the agent should behave in various situations]
- How to handle ambiguous requests
- How to respond to errors
- How to escalate complex issues
- How to maintain context

## 3. Integration

### How to Call:
[Describe how the orchestrator or other agents should invoke this agent]
- When to call this agent
- What conditions warrant its activation
- How to pass control to this agent

### Input Format:
[Define the structure of data this agent expects to receive]
```json
{
  "user_input": "string",
  "user_id": "string",
  "conversation_context": {
    "previous_messages": "array",
    "current_topic": "string",
    "entities": "object"
  }
}
```

### Output Format:
[Define the structure of data this agent returns]
```json
{
  "action": "string",
  "result": "object",
  "next_agent": "string or null",
  "context_updates": "object"
}
```

### Required Tools:
[List the MCP tools or other resources this agent needs access to]
- Tool 1
- Tool 2
- Tool 3

## 4. Examples

### Example 1:
**Input:** [User input scenario]
**Agent Response:** [How the agent should respond]
**Rationale:** [Why this is the appropriate response]

### Example 2:
**Input:** [Different user input scenario]
**Agent Response:** [How the agent should respond]
**Rationale:** [Why this is the appropriate response]

### Example 3:
**Input:** [Edge case or complex scenario]
**Agent Response:** [How the agent should respond]
**Rationale:** [Why this is the appropriate response]

## 5. Error Handling

### Common Error Scenarios:
[List typical error conditions and how to handle them]
- Error scenario 1: [Description and response]
- Error scenario 2: [Description and response]
- Error scenario 3: [Description and response]

### Fallback Procedures:
[Define what the agent should do when it encounters problems]
- When input is unclear
- When required tools are unavailable
- When context is insufficient
- When user intent is ambiguous

## 6. Testing

### Test Scenarios:
[Provide test cases to validate agent behavior]
- **Scenario 1:** [Normal operation case]
  - Input: [Sample input]
  - Expected Output: [Expected response]
  - Success Criteria: [How to measure success]

- **Scenario 2:** [Edge case]
  - Input: [Sample input]
  - Expected Output: [Expected response]
  - Success Criteria: [How to measure success]

- **Scenario 3:** [Error condition]
  - Input: [Sample input]
  - Expected Output: [Expected response]
  - Success Criteria: [How to measure success]

### Expected Behavior:
[Define the key behavioral patterns to validate]
- Response time requirements
- Accuracy expectations
- Context handling standards
- Error recovery patterns
- Communication style consistency

## 7. Performance Requirements

### Response Time:
[Define acceptable response time limits]
- Target: [Time limit for typical responses]
- Maximum: [Time limit before timeout]

### Accuracy:
[Define accuracy expectations]
- Intent recognition rate: [Percentage target]
- Context retention rate: [Percentage target]
- Error rate: [Maximum acceptable percentage]

### Resource Usage:
[Define resource consumption limits]
- Memory usage: [Maximum acceptable usage]
- API call limits: [Rate limiting requirements]

## 8. Security & Privacy

### Data Handling:
[Define how the agent should handle sensitive information]
- What data can be stored
- What data should be sanitized
- How to handle PII
- Logging restrictions

### Access Control:
[Define access and permission requirements]
- Authentication requirements
- Authorization checks
- Data isolation rules
- Permission escalation procedures

---

## Instructions for Use:

1. Copy this template to create a new agent specification file
2. Replace all bracketed placeholders with specific information for your agent
3. Customize each section to match your agent's specific requirements
4. Review and validate that all sections are properly filled out
5. Use the completed specification to guide implementation
6. Update the template as needed based on implementation feedback

This template provides a comprehensive structure for defining sub-agents that maintain consistency with the overall system architecture while allowing for specific customization based on individual agent requirements.