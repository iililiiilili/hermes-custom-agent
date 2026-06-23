# MVP Boundaries

## MVP Goal

The MVP should prove that a professional can finish one repeated office workflow faster on day one. It should not try to become a full practice-management system, document-management system, accounting system, or legal research platform.

## Common MVP Workflow

Every first-pack workflow should follow the same shape:

1. User selects a profession pack.
2. User adds files or notes.
3. App stores the work locally.
4. User chooses a task.
5. App produces a reviewable summary, checklist, or draft.
6. User edits, exports, or copies the result.
7. App shows subscription and usage status.

## Accountant MVP

First practical accountant workflows:

- Missing receipt and document checklist
- Filing-deadline checklist
- Client reply draft for missing materials
- Monthly or quarterly client status summary
- Basic file naming and folder organization suggestions

Accountant MVP should support:

- local vault for client files and notes
- manual file or text input
- checklist generation
- client-facing draft generation
- saved local outputs
- license and device status display

Out of scope for accountant MVP:

- direct tax filing
- bank feeds
- payroll execution
- accounting ledger sync
- automatic government portal submission
- firm-wide admin console
- guaranteed tax/legal judgment

## Lawyer MVP

First practical lawyer workflows:

- Matter summary from notes and documents
- Consultation memo cleanup
- Deadline and next-action checklist
- Client guidance or status update draft
- Evidence/document naming and version organization suggestions

Lawyer MVP should support:

- local matter workspace
- manual notes and file input
- document summarization
- checklist generation
- client-facing draft generation
- saved local outputs

Out of scope for lawyer MVP:

- legal advice without attorney review
- court e-filing
- full case-management replacement
- legal research database integration
- citation validation
- discovery automation
- trust accounting

## Shared Non-Goals

The first MVP should not include:

- generic chatbot positioning
- many verticals at once
- complex dashboards
- cloud-only document storage
- GPU or self-hosted model infrastructure
- heavy integrations before workflow validation
- mobile apps

## First Success Criteria

The MVP is working when:

- one accountant can complete a missing-document workflow from local files to client reply draft
- one lawyer can turn matter notes into a summary and next-action checklist
- seat/device licensing blocks unlicensed use cleanly
- the user can understand that LLM usage is included in the plan
- sensitive files are not uploaded by default
