# Business Agent Scaffold

This folder is the first business scaffold for a personal agent product aimed at accountants first, then lawyers. It turns the vertical-agent product notes into a reviewable business outline: what the product is, how it is packaged, what the MVP should include, and what should stay out until later.

## Product Position

The product is a local-first Windows desktop agent with a cloud control plane.

Users install the app, sign in, choose their profession pack, and run repeatable office workflows such as document summaries, missing-item checks, deadline checklists, and client reply drafts. The app is not positioned as a generic chatbot or developer tool. It is positioned as a practical assistant for reducing repetitive professional office work.

## Initial Verticals

1. Accountants and tax preparers
2. Small accounting offices
3. Solo lawyers and small law offices

Accountants are the first launch target because the repeated document, receipt, filing-deadline, and client-follow-up workflows are clear and frequent. Lawyers are the second target because matter summaries, consultation notes, deadline tracking, evidence organization, and client guidance drafts use the same core workflow model.

## Core Business Assumptions

- Sensitive files and notes should stay local by default.
- The cloud service should handle account, license, seat, device, billing, pack delivery, usage, and model routing.
- The default subscription includes LLM usage, so non-technical users do not need to bring API keys.
- BYOK is available only as an advanced option for users who explicitly want to manage their own model provider.
- Pricing follows the source-doc $10 / $29 / $50 ladder. If internal notes shorten this as "0 / 9 / 0", treat that as shorthand for the same Starter / Pro / Office ladder, not a separate pricing model.
- Licensing is based on seats and devices, so solo users and small offices can understand what they are buying.

## Documents

- `ARCHITECTURE.md`: product and business architecture
- `MVP_BOUNDARIES.md`: first practical accountant and lawyer MVP scope
- `PRICING.md`: subscription, seat/device licensing, and LLM cost policy
- `IMPLEMENTATION_PLAN.md`: staged plan from review scaffold to first usable MVP
