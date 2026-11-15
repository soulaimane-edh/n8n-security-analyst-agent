# Architecture and data flow

## Purpose

Provide an Outlook-centered email triage automation that retrieves VirusTotal signals for URL candidates and attachments, summarizes them with a Gemini language model, and sends an email report. The workflow is not an intrusion detection system, mail gateway or antivirus engine.

## Components

| Layer | n8n nodes | Responsibilities |
| --- | --- | --- |
| Ingestion | On New Email, Workflow Configuration, Filter Self Emails | Outlook polling and reporting-loop avoidance |
| Parsing | Extract URLs and Attachments, Route by Content Type | Detect rudimentary URL candidates and attachment presence |
| URL path | Process URLs for Scanning → Submit URL to VirusTotal → Wait for URL Analysis → Get URL Analysis Results | Submit and query URL analyses |
| File path | Get Attachments List → Process Attachments for Scanning → Download Attachment → Calculate File Hash → Check File Hash in VirusTotal → Restore Binary Context → Upload File to VirusTotal → Wait for File Analysis → Get File Analysis Results | Retrieve files, compute hash, query and submit content |
| Aggregation | Merge All Results, Aggregate Scan Results | Join scan responses and attempt metadata recovery |
| AI review | Security Analyst Agent, Google Gemini | Render an HTML interpretation from returned evidence |
| Output | No Threats Found, Send Security Report Email | Deliver message to reporting recipient |

The supplied workflow currently contains **24 nodes**, including a single Google Gemini model. A screenshot supplied in the original repository may represent an earlier edit and should not be treated as a diagram of the current model wiring.

## Trust boundaries

1. **Outlook → n8n:** message bodies and metadata originate outside the application and can contain attacker-controlled content.
2. **n8n → VirusTotal:** submitting URLs or file bytes transfers data to a third party, potentially with sharing and retention consequences.
3. **VirusTotal → Gemini:** external scan findings are used to prompt an LLM; treat those findings as evidence, not executable instructions.
4. **Gemini → Outlook:** AI-generated HTML is sent to a recipient; output escaping, authorization and data minimization are important.

## Known limitations

1. **No verified runtime test:** static tests verify export integrity, not Outlook, VirusTotal or Gemini behavior.
2. **Fixed wait times:** 15 seconds may not be enough. An analysis may still be queued or incomplete.
3. **File hash lookup is not a cache bypass:** the current graph queries hashes then still proceeds to file upload; it does not have a conditional 'known hash' skip.
4. **Privacy:** auto-upload of attachments can disclose private content to the external scanner. Standard uploads are not private scans.
5. **Simple URL parsing:** regex matching may capture punctuation, truncated URLs or HTML-encoded artifacts; it does not resolve redirect chains safely.
6. **Aggregation and mapping:** multiple URL/file items and parallel branches may not always preserve one-to-one metadata mappings; filename assignment is heuristic.
7. **Error handling:** explicit 401, 429, 5xx, timeout, retry and quota handling is incomplete. A missing path may lead to no report.
8. **LLM output:** model-generated status classifications can be wrong or manipulated; use grounded evidence and human review.
9. **Outlook body differences:** raw trigger payload variants may need field mapping adjustment for a particular account or n8n version.
10. **Third-party model:** the export references `gemini-1.5-flash`; model availability and pricing can change.
11. **Score semantics:** the presence of a detection is not conclusive proof of malware, and zero detections is not proof of safety.

## Recommended upgrade backlog

**P0 — before sensitive or commercial use:** gated file uploads with user consent; a licensed VirusTotal plan; credential management; end-to-end integration tests; reliable verdict states for failures and pending responses.

**P1 — correctness:** per-message aggregation keyed by Outlook message ID; exact attachment result mapping; asynchronous polling with maximum retry/timeout; backoff/rate limiting; HTML escaping and structured report schema.

**P2 — usability:** dashboard, structured audit trail with redaction, confidence/explanations, configurable severity, external ticketing, multi-tenant access controls, and observability.
