# How to use this skill

Use the skill when a user wants assistance with a **workflow that they are authorized to manage**, not to access arbitrary mailboxes or scan files without consent.

## Supported requests

- Explain the import and service-account requirements for `workflow.json`.
- Review a redacted n8n execution trace or a redacted VirusTotal response and identify pending, error and inconclusive results.
- Walk through a small test case using a synthetic message and a harmless dummy attachment.
- Propose safe, version-specific improvements for error handling and result correlation.

## Not supported without additional integration

- Reading or sending Outlook mail directly.
- Running a hosted n8n workflow on behalf of the user.
- Providing free access to VirusTotal or Google Gemini.
- Guaranteeing that all dangerous emails will be detected.

## Cautious result vocabulary

| Evidence | Recommended wording |
| --- | --- |
| Explicit completed response with no positive detections | No detections reported; still not proof of safety |
| Positive malicious/suspicious engine counts | Flagged for analyst review |
| Pending, malformed, unavailable or API error | Inconclusive — analysis incomplete |
| No URLs or attachments recognized | No scannable indicators found; message not fully assessed |

Refer to `references/security.md` for sensitive data handling and licensing obligations.
