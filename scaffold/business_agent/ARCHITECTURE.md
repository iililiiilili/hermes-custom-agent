# Architecture

## Model

The product uses a local-first app with a cloud control plane.

```text
Windows desktop app
  - local vault
  - profession packs
  - document and note workflows
  - generated summaries, checklists, and drafts

Cloud control plane
  - auth and subscription status
  - seat and device licensing
  - billing
  - pack availability and version metadata
  - usage metering
  - LLM routing and cost controls
```

## Local-First Responsibilities

The desktop app owns sensitive professional work data by default:

- client notes
- uploaded files
- extracted document text
- draft replies
- generated summaries
- task history
- local search indexes

The working promise is simple: files and notes stay on the user's PC unless the user explicitly enables sync, backup, or another cloud feature.

## Cloud Control Plane Responsibilities

The cloud service should avoid becoming the system of record for sensitive documents in the MVP. It should handle the operational parts needed to sell and run the product:

- account creation and login
- plan and subscription status
- seat limit and active device checks
- device registration and release
- profession pack list and versions
- LLM provider routing
- usage and soft-limit tracking
- payment events and renewal state

## LLM Policy

The default product includes LLM usage inside the subscription. The user should not need to create an API key, choose a provider, or understand token pricing.

The cloud control plane routes LLM calls through managed providers. It should prefer lower-cost models for routine summarization and drafting, with fallback rules for provider failure and higher-quality models for harder tasks.

BYOK is an advanced option, not the default plan. It can be offered later for power users or firms that require a specific provider account.

## Profession Packs

Each vertical is delivered as a pack:

- system prompts
- task templates
- allowed workflow actions
- output formats
- safety and review rules
- example checklists

Initial packs:

- `accounting_pack`
- `law_pack`
- `common_office_pack`

The common pack should contain reusable workflows: summarize notes, sort files, create checklists, draft client replies, and track deadlines.

## Licensing Surface

Licensing is enforced through both seats and devices.

- A seat represents a paid human user.
- A device represents an installed app instance that can run licensed workflows.
- Solo plans can be one seat and one device.
- Office plans can bundle multiple seats or devices.
- Additional seats/devices can be priced later after MVP validation.
