# Implementation Plan

## Phase 1: Business and Workflow Lock

Deliverables:

- confirm the accountant-first positioning
- choose one accountant workflow and one lawyer workflow
- write workflow scripts for input, processing, output, and review
- finalize first pricing copy using the $10 / $29 / $50 ladder
- define seat/device licensing rules in plain language

Exit criteria:

- the first accountant task and first lawyer task are named and bounded
- the user-facing security promise is written clearly
- pricing and included LLM policy are consistent across docs

## Phase 2: Product Skeleton

Deliverables:

- desktop app shell
- login and subscription status display
- profession pack selector
- local workspace and vault concept
- manual file or note input
- output view for summaries, checklists, and drafts

Exit criteria:

- a user can sign in, choose a pack, add local input, and see a generated result area
- no sensitive documents are stored in the cloud by default

## Phase 3: Control Plane MVP

Deliverables:

- auth bootstrap
- login and refresh
- license lookup
- device register and release
- pack list and pack metadata
- task preview and task run endpoint shape
- usage lookup

Exit criteria:

- an active license can use the app
- an expired or over-limit license is blocked cleanly
- pack availability can be controlled from the server

## Phase 4: LLM Routing and Included Usage

Deliverables:

- managed provider integration
- cheap-first model route for routine summaries and drafts
- fallback provider/model policy
- per-task cost estimate
- usage event logging
- fair-use soft limit rules

Exit criteria:

- default users can run workflows without API keys
- the system can estimate and record cost per task
- BYOK remains outside the default user journey

## Phase 5: First Accountant Workflow

Deliverables:

- missing receipt/document checklist
- filing-deadline checklist
- client reply draft
- local save/export of generated output

Exit criteria:

- an accountant can turn local client files or notes into a missing-item checklist and client reply draft
- the workflow is useful without integrations

## Phase 6: First Lawyer Workflow

Deliverables:

- matter summary
- consultation memo cleanup
- deadline and next-action checklist
- client status/guidance draft

Exit criteria:

- a lawyer can turn matter notes or documents into a summary, checklist, and draft
- the output is clearly framed for professional review

## Phase 7: Pilot Readiness

Deliverables:

- onboarding copy
- local-first security copy
- pricing page draft
- support notes for device changes
- pilot feedback checklist

Exit criteria:

- 3 to 5 accountant users can test the product
- 1 to 2 lawyer users can test the second pack
- feedback can be tied to specific repeated workflows, not general AI interest
