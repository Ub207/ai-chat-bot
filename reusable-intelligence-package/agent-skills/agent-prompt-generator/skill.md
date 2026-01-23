# Agent Prompt Generator Skill

## Skill Overview

**Name**: Agent Prompt Generator
**Category**: AI Development Tools
**Purpose**: Generate optimized system prompts for sub-agents based on specifications
**Reusability**: High - Applicable to any agent prompt generation scenario

## Purpose

This skill enables the automatic generation of optimized, comprehensive system prompts for sub-agents based on structured specifications. It ensures consistency in agent behavior, proper role definition, and effective instruction formulation while maintaining adherence to the project's conversational AI standards.

## Input Format

The skill accepts YAML specifications in the following format:

```yaml
agent:
  name: "Agent Name"
  role: "Brief description of the agent's primary role"
  capabilities:
    - "Capability 1"
    - "Capability 2"
    - "Capability 3"
  tools:
    - "tool_name_1"
    - "tool_name_2"
    - "tool_name_3"
  examples:
    - input: "Example user input"
      output: "Expected agent response"
    - input: "Another example input"
      output: "Another expected response"
  personality: "Personality traits and communication style"
  constraints: "Specific limitations or rules the agent must follow"
  error_handling: "How the agent should handle errors or unknown requests"
```

### Example Input:
```yaml
agent:
  name: "Task Creation Agent"
  role: "Specializes in processing user requests to create new tasks"
  capabilities:
    - "Parse natural language requests for task creation"
    - "Extract task parameters (title, description, due date, priority)"
    - "Validate extracted information meets requirements"
    - "Request missing information from users"
  tools:
    - "add_task"
    - "list_tasks"
  examples:
    - input: "Add a task to buy groceries"
      output: "I've created a task: 'buy groceries'. Is there anything else you'd like to add to this task?"
    - input: "Remind me to call my mom tomorrow at 6pm"
      output: "I've created a task: 'call my mom' with a due date of tomorrow at 6pm."
  personality: "Helpful, patient, clear, positive"
  constraints: "Must validate all required fields before creating tasks"
  error_handling: "Ask for clarification when user input is ambiguous"
```

## Output Format

The skill generates a complete system prompt including:

### 1. Role Definition Section
- Clear statement of the agent's primary function
- Description of the agent's scope and boundaries
- Explanation of how the agent fits into the overall system

### 2. Capability Instructions
- Detailed explanation of each capability
- Step-by-step instructions for executing each capability
- Contextual guidance for when to use each capability

### 3. Tool Usage Guidelines
- Specific instructions for when and how to use each tool
- Parameters required for each tool
- Expected outcomes from each tool

### 4. Behavioral Instructions
- Communication style and tone guidelines
- Personality traits to embody
- Interaction patterns to follow

### 5. Example Demonstrations
- Formatted examples showing proper input-output patterns
- Context for when to apply similar responses
- Variations to demonstrate flexibility

### 6. Constraint Enforcement
- Clear boundaries and limitations
- Error conditions to avoid
- Fallback behaviors when constraints are reached

### 7. Error Handling Protocols
- Specific procedures for different error types
- User communication during error states
- Recovery procedures and fallback options

## Generated Components

### Core Identity
- Agent's primary mission statement
- Role within the larger system context
- Key differentiators from other agents

### Instruction Hierarchy
- Primary instructions (must always follow)
- Secondary instructions (should generally follow)
- Tertiary instructions (nice to have but flexible)

### Response Framework
- Standard response patterns for common scenarios
- Personalization guidelines to match personality
- Context awareness instructions

### Validation Rules
- Input validation procedures
- Output quality checks
- Consistency verification

## Usage Scenarios

### Primary Use Case
- Generating initial prompts for new sub-agents
- Updating prompts when agent capabilities change
- Standardizing prompts across different agent types
- Creating consistent behavior patterns

### Integration Points
- Part of the agent development workflow
- Used when creating new specialized agents
- Applied during agent refactoring or capability expansion
- Integrated into the agent testing and validation process

## Quality Standards

### Effectiveness
- Clear role definition that aligns with specifications
- Comprehensive instruction coverage for all capabilities
- Appropriate balance of specificity and flexibility
- Effective error handling and fallback procedures

### Consistency
- Uniform structure across all generated prompts
- Consistent terminology and communication patterns
- Aligned personality traits across agents
- Standardized error handling approaches

### Performance
- Optimized for the target LLM's comprehension
- Clear instruction hierarchy to prevent confusion
- Proper formatting for maximum effectiveness
- Concise yet comprehensive guidance

## Reusability Factors

### Flexible Parameters
- Adaptable personality traits
- Configurable capability emphasis
- Extensible tool integration
- Customizable constraint sets

### Modular Design
- Separation of role definition, instructions, and examples
- Reusable constraint patterns
- Standardized error handling templates
- Common behavioral guidelines

### Scalability
- Support for complex multi-capability agents
- Extensible for new tool types
- Adaptable for different agent sizes and scopes
- Configurable for various use case requirements

## Validation Criteria

### Before Generation
- Specification completeness check
- Required fields presence validation
- Capability consistency verification
- Example quality assessment

### After Generation
- Prompt coherence evaluation
- Role-instruction alignment check
- Example-relevance verification
- Constraint-adherence confirmation

## Dependencies

### Required Components
- Project's agent architecture guidelines
- Standardized tool interfaces
- Error handling frameworks
- Personality and communication standards

### Assumptions
- Standard project agent patterns and conventions
- Available tools and their interfaces
- Consistent error handling approaches
- Established communication style guidelines