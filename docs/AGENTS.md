# Agent System Documentation

## Overview

The Todo App Chatbot utilizes a multi-agent architecture with a main orchestrator agent coordinating five specialized sub-agents. Each agent has a specific responsibility in the task management workflow, enabling sophisticated natural language processing and reliable task execution.

## Main Orchestrator Agent

### Responsibilities
- **Intent Recognition**: Analyzes user input to determine the appropriate action
- **Agent Routing**: Directs requests to the most suitable sub-agent
- **Context Management**: Maintains conversation state and user preferences
- **Fallback Handling**: Manages unrecognized intents and error recovery
- **Response Generation**: Composes coherent responses based on tool outputs

### Operation Flow
1. Receives user message from the chat endpoint
2. Analyzes the message to identify intent and entities
3. Selects the appropriate sub-agent based on the intent
4. Coordinates with the selected agent to execute the action
5. Formats the response for the user
6. Updates conversation context as needed

### Example Interaction
```
User: "I need to add a task to buy groceries tomorrow"
Orchestrator: Recognizes intent as "add_task"
→ Routes to Task Management Agent
← Receives confirmation of task creation
→ Generates response: "I've created a task: 'buy groceries' for tomorrow."
```

## Sub-Agent Descriptions

### 1. Task Management Agent

#### Purpose
Handles all CRUD operations for tasks including creation, retrieval, updating, and deletion.

#### Capabilities
- Create new tasks from natural language input
- Retrieve task lists with filtering options
- Update task properties (title, priority, due date, etc.)
- Mark tasks as completed
- Delete tasks with confirmation

#### MCP Tools Utilized
- `add_task`: Creates new tasks with validation
- `list_tasks`: Retrieves filtered task lists
- `complete_task`: Marks tasks as completed
- `update_task`: Modifies task properties
- `delete_task`: Removes tasks from the system

#### Example Interactions
```
User: "Add a task to schedule dentist appointment for Friday"
Agent: { "action": "add_task",
         "params": {"title": "schedule dentist appointment",
                    "due_date": "2026-01-16",
                    "priority": "medium"} }

User: "Show me all high priority tasks"
Agent: { "action": "list_tasks",
         "params": {"priority": "high",
                    "status": "pending"} }
```

### 2. Natural Language Understanding (NLU) Agent

#### Purpose
Processes natural language input to extract structured data and identify user intentions.

#### Capabilities
- **Entity Extraction**: Identifies dates, priorities, categories, and task details
- **Intent Classification**: Determines the user's desired action
- **Contextual Understanding**: Recognizes references to previous interactions
- **Ambiguity Resolution**: Handles unclear or incomplete requests

#### Techniques Used
- Named Entity Recognition (NER)
- Dependency parsing
- Semantic analysis
- Context window management

#### Example Interactions
```
User: "Remind me to call mom next Tuesday at 3 PM"
NLU: { "intent": "add_task",
       "entities": {
         "task": "call mom",
         "date": "2026-01-20",
         "time": "15:00",
         "priority": "medium"
       }}

User: "Change the grocery task to high priority"
NLU: { "intent": "update_task",
       "entities": {
         "task_reference": "grocery",
         "property": "priority",
         "value": "high"
       }}
```

### 3. Context Awareness Agent

#### Purpose
Maintains and manages conversation context to enable coherent multi-turn interactions.

#### Capabilities
- **Reference Resolution**: Links pronouns and references to specific tasks/conversations
- **Context Persistence**: Maintains relevant information across turns
- **History Management**: Stores and retrieves conversation history
- **User Profile Management**: Tracks user preferences and patterns

#### Context Elements Tracked
- Previously mentioned tasks
- Current conversation topic
- User preferences and habits
- Recent system responses
- Temporal context for date/time references

#### Example Interactions
```
User: "I need to add a task to buy milk"
System: "Added task: Buy milk"
User: "Make it urgent"  // Refers to the previous task
Context Agent: Links "it" to "buy milk" task
→ Updates task priority to "high"
```

### 4. Validation Agent

#### Purpose
Ensures all operations comply with business rules and data integrity requirements.

#### Capabilities
- **Input Validation**: Verifies data formats and ranges
- **Business Rule Enforcement**: Checks for logical consistency
- **Permission Verification**: Validates user authorization
- **Data Integrity Checks**: Ensures referential integrity

#### Validation Rules
- Task titles must be 1-200 characters
- Dates must be in valid ISO 8601 format
- Priorities must be "low", "medium", or "high"
- Users can only modify their own tasks
- Task statuses must be valid ("pending", "in_progress", "completed", "cancelled")

#### Example Interactions
```
User: "Create task with priority 'urgent'"
Validation Agent: Rejects - invalid priority value
→ Returns error: "Priority must be 'low', 'medium', or 'high'"

User: "Complete task 12345"
Validation Agent: Checks if user owns task 12345
→ Proceeds if authorized, rejects if not
```

### 5. Error Handling Agent

#### Purpose
Manages system errors and provides graceful recovery mechanisms.

#### Capabilities
- **Error Classification**: Categorizes errors by type and severity
- **Recovery Strategies**: Implements appropriate recovery procedures
- **User Communication**: Provides clear error messages to users
- **Fallback Procedures**: Offers alternative solutions when primary actions fail

#### Error Categories
- **Validation Errors**: Invalid input data
- **Authorization Errors**: Insufficient permissions
- **System Errors**: Technical failures
- **Integration Errors**: External service issues
- **Business Logic Errors**: Violation of business rules

#### Example Interactions
```
System Error: Database connection failed
Error Handler: Initiates retry mechanism
→ If retries fail, informs user: "I'm experiencing technical difficulties. Please try again in a moment."

User: "Complete task 999999" (non-existent task)
Error Handler: Detects 404 error
→ Responds: "I couldn't find that task. Would you like me to list your tasks?"
```

## Agent Collaboration

### Communication Protocol
Agents communicate through a standardized message format that includes:
- Action type and parameters
- Context information
- Error indicators
- Metadata for coordination

### Workflow Coordination
1. **Orchestration**: Main agent coordinates the overall workflow
2. **Specialization**: Each sub-agent handles its specific domain
3. **Information Sharing**: Relevant context is shared between agents
4. **Consistency**: All agents maintain consistent user experience
5. **Feedback Loop**: Results are aggregated and presented coherently

### Example Multi-Agent Interaction
```
User: "I want to update my important meeting task to next week and mark it as high priority"

1. Orchestrator → NLU Agent:
   Analyze: "update important meeting task to next week and high priority"
   Result: {intent: "update_task", entities: {...}}

2. NLU Agent → Context Agent:
   Resolve: Which "meeting task" is referenced?
   Result: Task ID 456

3. Context Agent → Validation Agent:
   Validate: Update parameters are valid?
   Result: All parameters valid

4. Validation Agent → Task Management Agent:
   Execute: Update task 456 with new date and priority
   Result: Update successful

5. Task Management Agent → Orchestrator:
   Response: Task updated successfully
   Final Response to User: "I've updated your meeting task to next week with high priority."
```

## Performance Considerations

### Response Time Optimization
- Parallel processing where possible
- Caching frequently accessed data
- Efficient database queries
- Asynchronous operations for non-critical tasks

### Resource Management
- Connection pooling for database operations
- Memory management for context storage
- Load balancing across agent instances
- Circuit breakers for external dependencies

### Scalability Features
- Horizontal scaling capability
- Stateless agent design
- Distributed processing support
- Auto-scaling based on load