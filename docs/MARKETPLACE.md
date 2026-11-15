# Agent skill marketplace readiness

## Current state

This repository includes a **SKILL.md scaffold**, not a turnkey agent runtime. The underlying system is an n8n workflow requiring Outlook, VirusTotal and Google Gemini credentials and the deployer's own runtime. Do not advertise it as an autonomous hosted analyzer or as providing VirusTotal calls for free.

## Build the package

```bash
python scripts/package_skill.py
```

Output: `dist/email-threat-triage-skill.zip`. The ZIP contains the root `SKILL.md` and `workflow.json`, plus setup/privacy references. It contains no binary files or secrets.

Agensi documentation: https://www.agensi.io/docs/packaging

## Commercial deployment blockers

1. **VirusTotal license:** the free/public API **prohibits commercial products/services**. Obtain a valid commercial agreement, or redesign the integration to use an appropriate authorized threat intelligence provider.
2. **Data privacy:** introduce an opt-in policy for transmitting attachments, or remove the automatic upload capability before marketing to customers.
3. **Validation:** test the exact JSON on a supported n8n version and credential setup using several mail scenarios, API error responses, and queued scans.
4. **Secrets:** replace inline keys and use credential vaults for platforms that do not support the `$env` expression.
5. **Observability:** establish truthful inconclusive results, rate limiting, execution correlation, timeout behavior, and support documentation.
6. **User promises:** state external paid requirements and the fact that the skill guides an authorized operator; do not claim one-click deployment or guaranteed detection.
7. **Seller rights:** confirm rights to any external logos, screenshots, code, service names or library dependencies reused in the product.

## Suggested listing copy (only after blockers are resolved)

**Title:** n8n Email Threat Triage Assistant

**Summary:** An agent skill that helps you deploy and review an n8n workflow connecting Outlook, VirusTotal threat intelligence and a Gemini-based security report. Requires your own authorized n8n instance and provider accounts.

**Target audience:** SOC analysts, security automation engineers and n8n builders who want a configurable reference implementation.

**Not included:** hosted n8n execution, provider API subscriptions, Outlook accounts, guaranteed malware detection, or private file scanning.

## Packaging specifications

Agensi finds `SKILL.md` inside an uploaded ZIP and requires `name` in its YAML frontmatter; `description` is recommended. Avoid executable bundles and secrets. See https://www.agensi.io/docs/packaging for current requirements.
