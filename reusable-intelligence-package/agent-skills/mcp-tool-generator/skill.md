# MCP Tool Generator Skill

## Skill Overview

**Name**: MCP Tool Generator
**Category**: Development Tools
**Purpose**: Generate complete MCP (Model Context Protocol) tool implementations from specifications
**Reusability**: High - Applicable to any MCP tool generation scenario

## Purpose

This skill enables the automatic generation of complete MCP tool implementations from high-level specifications. It streamlines the development process by creating standardized, validated tool implementations that conform to the project's architecture and coding standards.

## Input Format

The skill accepts specifications in the following markdown format:

```markdown
## Tool: tool_name
Purpose: [Brief description of what the tool does]
Parameters:
- param1: [description] (type, required/optional)
- param2: [description] (type, required/optional)
Returns: [description of return value and type]
Error Cases: [description of possible errors]
```

### Example Input:
```markdown
## Tool: add_task
Purpose: Create a new task in the system
Parameters:
- user_id: Unique identifier of the user (string, required)
- title: Title of the task (string, required, 1-200 chars)
- description: Optional task description (string, optional)
- priority: Task priority level (string, optional, default: "medium")
Returns: Object with task_id, status, and title
Error Cases: Invalid title, unauthorized access, database error
```

## Output Format

The skill generates a complete MCP tool implementation including:

### 1. JSON Schema Definition
- Complete JSON schema for input validation
- Property definitions with types, constraints, and descriptions
- Required field specifications
- Additional properties restrictions

### 2. Python Function Implementation
- Function signature with proper type hints
- Input validation using Pydantic or similar
- Business logic implementation
- Database interaction patterns
- Return value formatting

### 3. Error Handling Code
- Custom exception classes for specific error cases
- Error response formatting
- Logging patterns for debugging
- Graceful degradation strategies

### 4. Database Integration
- SQLModel/SQLAlchemy model interactions
- Session management patterns
- Transaction handling
- Data validation and sanitization

## Generated Components

### Function Structure
- Type-annotated function definition
- Docstring with purpose and parameter descriptions
- Input validation using Pydantic models
- Business logic execution
- Result formatting and return

### Validation Layer
- Input parameter validation
- Type checking and conversion
- Range and format validation
- Business rule validation

### Error Handling
- Specific exception handling for different error cases
- User-friendly error messages
- System error logging
- Graceful fallback mechanisms

### Security Measures
- User authentication verification
- Data access authorization
- Input sanitization
- SQL injection prevention

## Usage Scenarios

### Primary Use Case
- Rapid development of MCP tools from specifications
- Consistent implementation patterns across all tools
- Reduced manual coding errors
- Standardized error handling and validation

### Integration Points
- Part of the development workflow for creating new tools
- Used by the orchestrator agent for dynamic tool creation
- Integrated into the CI/CD pipeline for automated tool generation
- Applied when extending the system with new functionality

## Quality Standards

### Code Quality
- Follows project's coding standards and conventions
- Includes comprehensive type annotations
- Contains proper documentation and examples
- Implements proper error handling and logging

### Security Compliance
- Validates all user inputs
- Implements proper authentication checks
- Prevents unauthorized data access
- Sanitizes all external inputs

### Performance Considerations
- Efficient database queries
- Proper session management
- Optimized error handling paths
- Minimal resource usage

## Reusability Factors

### Adaptable Parameters
- Flexible parameter definitions
- Configurable validation rules
- Extensible return value formats
- Customizable error cases

### Modular Design
- Separation of validation, business logic, and error handling
- Reusable validation patterns
- Common error handling utilities
- Standardized database interaction patterns

### Scalability
- Support for complex parameter structures
- Extensible for new error types
- Adaptable for different database schemas
- Configurable for various use cases

## Validation Criteria

### Before Generation
- Specification format validation
- Required fields presence check
- Parameter type consistency
- Error case completeness

### After Generation
- Generated code syntax validation
- Type hint correctness
- Schema validation accuracy
- Error handling completeness

## Dependencies

### Required Components
- Project's database models
- Authentication/authorization system
- Logging infrastructure
- Error handling utilities

### Assumptions
- Standard project structure and conventions
- Available database connection
- Proper authentication mechanisms
- Existing model definitions