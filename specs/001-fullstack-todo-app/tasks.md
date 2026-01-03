---
description: "Task list for Full Stack Todo Application implementation"
---

# Tasks: Full Stack Todo Application

**Input**: Design documents from `/specs/001-fullstack-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Test tasks are included per your request for backend route tests, DB tests, and basic UI tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`, `backend/alembic/`
- **Frontend**: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

### Directory Structure

- [ ] T001 Create `backend/` directory with `src/` subdirectories (models, schemas, services, api/routes, db)
- [ ] T002 Create `frontend/` directory with `src/` subdirectories (components, pages, services, types, styles)

### Backend Setup

- [ ] T003 Initialize Python virtual environment for backend
- [ ] T004 Create `backend/requirements.txt` with FastAPI, SQLAlchemy, Pydantic, asyncpg, uvicorn, alembic, pytest
- [ ] T005 Create `backend/pyproject.toml` with project metadata and Black configuration
- [ ] T006 Configure Black and flake8 for backend linting in `backend/pyproject.toml`

### Frontend Setup

- [ ] T007 [P] Initialize Next.js project with TypeScript: `npx create-next-app@latest frontend --typescript --tailwind`
- [ ] T008 [P] Configure ESLint and Prettier for frontend in `frontend/` directory
- [ ] T009 Set up Tailwind CSS configuration in `frontend/tailwind.config.js`

### Git Configuration

- [ ] T010 Create `.pre-commit-config.yaml` with hooks for Black, flake8, ESLint

**Checkpoint**: Project structure ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Setup

- [ ] T011 Create Neon PostgreSQL database and retrieve connection URL
- [ ] T012 Create `backend/.env` with `DATABASE_URL=postgresql://...` (Neon connection string)
- [ ] T013 Create `backend/src/db/connection.py` with async SQLAlchemy connection and session dependency

### Backend Foundation

- [ ] T014 [P] Create SQLAlchemy Base class in `backend/src/db/__init__.py`
- [ ] T015 [P] Create `backend/src/schemas/__init__.py` for Pydantic schema exports
- [ ] T016 [P] Create `backend/src/models/__init__.py` for model exports
- [ ] T017 [P] Create `backend/src/services/__init__.py` for service exports
- [ ] T018 [P] Create `backend/src/api/__init__.py` and `backend/src/api/routes/__init__.py`
- [ ] T019 Initialize Alembic for migrations: `cd backend && alembic init alembic`
- [ ] T020 Create initial Alembic migration script for todos table
- [ ] T021 Create `backend/src/main.py` FastAPI application with CORS configuration
- [ ] T022 Create health check endpoint `GET /health` in `backend/src/main.py`

### Error Handling Infrastructure

- [ ] T023 Create standardized error response schema in `backend/src/schemas/error.py`
- [ ] T024 Create HTTP exception handler in `backend/src/main.py` for consistent error responses

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and List Todos (Priority: P1) MVP

**Goal**: Users can create new todos and view all todos

**Independent Test**: Create a todo via UI → Verify it appears in list with correct title

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T025 [P] [US1] Contract test for POST /api/todos in `backend/tests/contract/test_create_todo.py`
- [ ] T026 [P] [US1] Contract test for GET /api/todos in `backend/tests/contract/test_list_todos.py`
- [ ] T027 [P] [US1] Integration test for create todo journey in `backend/tests/integration/test_create_todo.py`

### Backend Implementation

- [ ] T028 [P] [US1] Create Todo SQLAlchemy model in `backend/src/models/todo.py`
- [ ] T029 [P] [US1] Create TodoCreate Pydantic schema in `backend/src/schemas/todo.py`
- [ ] T030 [P] [US1] Create TodoResponse Pydantic schema in `backend/src/schemas/todo.py`
- [ ] T031 [US1] Implement TodoService with create() method in `backend/src/services/todo_service.py`
- [ ] T032 [US1] Implement TodoService with list() method in `backend/src/services/todo_service.py`
- [ ] T033 [US1] Create POST /api/todos endpoint in `backend/src/api/routes/todos.py`
- [ ] T034 [US1] Create GET /api/todos endpoint in `backend/src/api/routes/todos.py`
- [ ] T035 [US1] Register router in `backend/src/main.py`

### Frontend Implementation

- [ ] T036 [P] [US1] Create TypeScript Todo type in `frontend/src/types/todo.ts`
- [ ] T037 [P] [US1] Configure axios API client in `frontend/src/services/api.ts`
- [ ] T038 [US1] Create TodoForm component in `frontend/src/components/TodoForm.tsx`
- [ ] T039 [US1] Create TodoList component in `frontend/src/components/TodoList.tsx`
- [ ] T040 [US1] Create API functions createTodo() and getTodos() in `frontend/src/services/todo.ts`
- [ ] T041 [US1] Implement index page in `frontend/src/pages/index.tsx`

**Checkpoint**: User Story 1 complete - can create and list todos

---

## Phase 4: User Story 2 - Update Todos (Priority: P1)

**Goal**: Users can edit todo title, description, and mark as complete

**Independent Test**: Edit existing todo → Verify changes persist in database

### Tests for User Story 2

- [ ] T042 [P] [US2] Contract test for PUT /api/todos/{id} in `backend/tests/contract/test_update_todo.py`
- [ ] T043 [P] [US2] Integration test for update todo journey in `backend/tests/integration/test_update_todo.py`

### Backend Implementation

- [ ] T044 [P] [US2] Create TodoUpdate Pydantic schema in `backend/src/schemas/todo.py`
- [ ] T045 [US2] Add update() method to TodoService in `backend/src/services/todo_service.py`
- [ ] T046 [US2] Add get_by_id() method to TodoService in `backend/src/services/todo_service.py`
- [ ] T047 [US2] Create GET /api/todos/{id} endpoint in `backend/src/api/routes/todos.py`
- [ ] T048 [US2] Create PUT /api/todos/{id} endpoint in `backend/src/api/routes/todos.py`

### Frontend Implementation

- [ ] T049 [P] [US2] Add updateTodo() API function in `frontend/src/services/todo.ts`
- [ ] T050 [P] [US2] Add getTodo() API function in `frontend/src/services/todo.ts`
- [ ] T051 [US2] Create TodoItem component with edit controls in `frontend/src/components/TodoItem.tsx`
- [ ] T052 [US2] Add toggle complete checkbox to TodoItem component
- [ ] T053 [US2] Add inline edit interface or modal to TodoItem component

**Checkpoint**: User Story 2 complete - can update todos

---

## Phase 5: User Story 3 - Delete Todos (Priority: P1)

**Goal**: Users can delete unwanted todos

**Independent Test**: Delete todo → Verify it no longer appears in list

### Tests for User Story 3

- [ ] T054 [P] [US3] Contract test for DELETE /api/todos/{id} in `backend/tests/contract/test_delete_todo.py`
- [ ] T055 [P] [US3] Integration test for delete todo journey in `backend/tests/integration/test_delete_todo.py`

### Backend Implementation

- [ ] T056 [US3] Add delete() method to TodoService in `backend/src/services/todo_service.py`
- [ ] T057 [US3] Create DELETE /api/todos/{id} endpoint in `backend/src/api/routes/todos.py`

### Frontend Implementation

- [ ] T058 [P] [US3] Add deleteTodo() API function in `frontend/src/services/todo.ts`
- [ ] T059 [US3] Add delete button to TodoItem component
- [ ] T060 [US3] Add confirmation dialog before delete action

**Checkpoint**: User Story 3 complete - can delete todos

---

## Phase 6: User Story 4 - Persistent Data Storage (Priority: P1)

**Goal**: Todos persist after page refresh and server restart

**Independent Test**: Create todos → Refresh page → Verify todos remain

### Database Testing

- [ ] T061 [P] [US4] Write unit tests for Todo model in `backend/tests/unit/test_todo_model.py`
- [ ] T062 [P] [US4] Write unit tests for TodoService in `backend/tests/unit/test_todo_service.py`
- [ ] T063 [P] [US4] Write integration tests for database operations in `backend/tests/integration/test_db_operations.py`

### Persistence Verification

- [ ] T064 [US4] Verify todos table has proper indexes (created_at, is_completed)
- [ ] T065 [US4] Test data persists across server restarts
- [ ] T066 [US4] Verify completion status is preserved after reload

**Checkpoint**: User Story 4 complete - data persists reliably

---

## Phase 7: User Story 5 - User-Friendly Interface (Priority: P2)

**Goal**: Clean, intuitive UI with visual feedback

**Independent Test**: New user completes workflow without confusion or assistance

### Frontend UX Improvements

- [ ] T067 [P] [US5] Add toast notifications for success/error feedback in `frontend/src/components/Toast.tsx`
- [ ] T068 [P] [US5] Create empty state placeholder when no todos exist
- [ ] T069 [P] [US5] Add loading skeletons during API calls
- [ ] T070 [US5] Improve form validation with clear error messages in TodoForm
- [ ] T071 [US5] Style buttons and inputs for better UX using Tailwind

### Accessibility

- [ ] T072 [P] [US5] Ensure keyboard navigation works for all interactive elements
- [ ] T073 [P] [US5] Add ARIA labels where appropriate

**Checkpoint**: User Story 5 complete - UI is user-friendly and accessible

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Testing completion and documentation

### Backend Testing

- [ ] T074 [P] Write schema validation tests in `backend/tests/unit/test_schemas.py`
- [ ] T075 [P] Run all backend tests with pytest and achieve >80% coverage
- [ ] T076 [P] Fix any failing tests and ensure all pass

### Frontend Testing

- [ ] T077 [P] Write unit tests for TodoForm component in `frontend/tests/components/TodoForm.test.tsx`
- [ ] T078 [P] Write unit tests for TodoList component in `frontend/tests/components/TodoList.test.tsx`
- [ ] T079 [P] Write unit tests for TodoItem component in `frontend/tests/components/TodoItem.test.tsx`
- [ ] T080 Run all frontend tests and ensure pass

### Documentation

- [ ] T081 Update `.specify/memory/constitution.md` with Phase-2 principles if needed
- [ ] T082 Update `quickstart.md` with actual commands for setup and running
- [ ] T083 Verify `contracts/api-endpoints.md` is complete with all endpoints
- [ ] T084 Create development workflow guide in `docs/DEVELOPMENT.md`
- [ ] T085 Document environment variables required in `.env.example`

**Checkpoint**: All documentation complete, all tests passing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phase 3-7 (User Stories)**: All depend on Phase 2 completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US5)
- **Phase 8 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (Create/List)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (Update)**: Can start after Phase 2 - Integrates with US1 components
- **User Story 3 (Delete)**: Can start after Phase 2 - Integrates with US1 components
- **User Story 4 (Persistence)**: Depends on US1, US2, US3 complete
- **User Story 5 (UX)**: Depends on US1 complete - can proceed in parallel with US2-US4

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Phase 1 tasks marked [P] can run in parallel
- All Phase 2 tasks marked [P] can run in parallel (within Phase 2)
- Once Phase 2 completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel

---

## Parallel Execution Examples

### User Story 1 (Create/List)

```bash
# Run all tests for User Story 1 together:
Task T025: Contract test for POST /api/todos
Task T026: Contract test for GET /api/todos
Task T027: Integration test for create journey

# Run model/schema creation in parallel:
Task T028: Create Todo SQLAlchemy model
Task T029: Create TodoCreate schema
Task T030: Create TodoResponse schema
```

### User Story 2 (Update)

```bash
# Run update tests in parallel:
Task T042: Contract test for PUT /todos/{id}
Task T043: Integration test for update journey

# Run update implementation in parallel:
Task T044: Create TodoUpdate schema
Task T045: Add update() to TodoService
Task T046: Add get_by_id() to TodoService
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready (minimum viable product)

### Incremental Delivery

1. Complete Phase 1 + Phase 2 → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Phase 8: Polish and finalize

### Parallel Team Strategy

With multiple developers:

1. Team completes Phase 1 + Phase 2 together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | 10 | Setup - Project structure and tooling |
| Phase 2 | 14 | Foundational - DB connection, FastAPI skeleton |
| Phase 3 (US1) | 17 | Create and List Todos |
| Phase 4 (US2) | 13 | Update Todos |
| Phase 5 (US3) | 7 | Delete Todos |
| Phase 6 (US4) | 6 | Persistent Data Storage |
| Phase 7 (US5) | 8 | User-Friendly Interface |
| Phase 8 | 12 | Polish & Cross-Cutting (Testing, Docs) |
| **Total** | **87** | All implementation tasks |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label (US1-US5) maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Write tests FIRST, ensure they FAIL before implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
