# Chatbot Database Schema Specification

## Overview

This specification defines the database schema for the Todo App Chatbot Phase III, focusing on conversation management and message storage while maintaining integration with existing task management functionality.

## New Tables

### Conversation Table

#### Fields
- **id**: Primary identifier for the conversation record
  - Type: Integer (Auto-incrementing)
  - Constraints: Primary Key, Not Null
- **user_id**: Identifier linking the conversation to a specific user
  - Type: String
  - Constraints: Not Null
- **created_at**: Timestamp when the conversation was initiated
  - Type: DateTime with timezone
  - Constraints: Not Null, Default to current timestamp
- **updated_at**: Timestamp when the conversation was last modified
  - Type: DateTime with timezone
  - Constraints: Not Null, Default to current timestamp, Updates automatically

#### Indexes
- **user_id**: Index on user_id field to optimize queries for user-specific conversations

#### Relationships
- **Has Many**: Messages (one conversation can have multiple messages)
- **Foreign Key**: None (this is the parent table in the conversation-message relationship)

### Message Table

#### Fields
- **id**: Primary identifier for the message record
  - Type: Integer (Auto-incrementing)
  - Constraints: Primary Key, Not Null
- **conversation_id**: Foreign key linking the message to a specific conversation
  - Type: Integer
  - Constraints: Not Null, Foreign Key to Conversation table
- **user_id**: Identifier of the user who sent the message
  - Type: String
  - Constraints: Not Null
- **role**: Defines the role of the message sender (user, assistant, system, tool)
  - Type: String
  - Constraints: Not Null, Valid values: "user", "assistant", "system", "tool"
- **content**: The actual content of the message
  - Type: Text
  - Constraints: Not Null
- **tool_calls**: Optional JSON string representing tool calls made in the message
  - Type: Text
  - Constraints: Nullable
- **created_at**: Timestamp when the message was created
  - Type: DateTime with timezone
  - Constraints: Not Null, Default to current timestamp

#### Indexes
- **conversation_id**: Index on conversation_id field to optimize queries for messages within a conversation
- **user_id**: Index on user_id field to optimize queries for messages from a specific user

#### Relationships
- **Belongs To**: Conversation (each message belongs to one conversation)
- **Foreign Key**: conversation_id references Conversation.id

## Existing Table Changes

### Task Table Modifications
- **Add Field**: conversation_id (Integer, Nullable)
  - Purpose: Link tasks to the conversation that created them
  - Type: Integer
  - Constraints: Nullable, Foreign Key to Conversation table
  - Index: Index on conversation_id field to optimize queries for tasks by conversation

### Additional Task Table Indexes
- **user_id**: Ensure index exists on user_id field for optimized user-specific queries
- **status**: Index on status field to optimize queries for active/completed tasks
- **due_date**: Index on due_date field to optimize date-based queries

## Queries Specification

### Get Conversation History
- **Purpose**: Retrieve all conversations for a specific user
- **Input**: user_id
- **Output**: List of conversations with metadata
- **Filtering**: By user_id
- **Ordering**: By created_at (descending)

### Get Messages in Conversation
- **Purpose**: Retrieve all messages within a specific conversation
- **Input**: conversation_id
- **Output**: List of messages in chronological order
- **Filtering**: By conversation_id
- **Ordering**: By created_at (ascending)

### Save Message
- **Purpose**: Create a new message record in a conversation
- **Input**: conversation_id, user_id, role, content, optional tool_calls
- **Output**: Created message record with timestamps
- **Validation**: Ensure conversation exists before creating message

### Create Conversation
- **Purpose**: Initialize a new conversation for a user
- **Input**: user_id
- **Output**: Created conversation record with timestamps
- **Default Values**: Set created_at and updated_at to current timestamp

## Constraints

### User Data Isolation
- **Constraint**: Each user can only access their own conversations and messages
- **Implementation**: All queries must filter by user_id
- **Validation**: Foreign key constraints ensure data integrity

### Foreign Key Constraints
- **Message to Conversation**: conversation_id in Message table must reference existing Conversation.id
- **Task to Conversation**: conversation_id in Task table must reference existing Conversation.id
- **Referential Integrity**: Prevent orphaned records by maintaining proper relationships

### Timestamp Constraints
- **Created At**: All records must have a created_at timestamp set at creation time
- **Updated At**: For conversation records, updated_at must update automatically when modified
- **Timezone**: All datetime fields must store timezone information for consistency across different locations

### Data Validation Constraints
- **Role Validation**: Message role field must be one of the allowed values ("user", "assistant", "system", "tool")
- **Required Fields**: All non-nullable fields must have values provided during insertion
- **Content Length**: Message content should have reasonable length limits to prevent abuse

## Performance Considerations

### Index Strategy
- Primary indexes on all foreign key fields for efficient joins
- Indexes on frequently queried fields (user_id, conversation_id)
- Composite indexes where appropriate for multi-field queries

### Data Partitioning
- Consider time-based partitioning for messages table as conversation volume grows
- Archive older conversations to separate tables if needed for performance

### Query Optimization
- Use indexed fields in WHERE clauses for optimal performance
- Limit result sets with pagination for large datasets
- Use appropriate JOIN strategies for related data retrieval