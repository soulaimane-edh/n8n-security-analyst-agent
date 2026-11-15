# Setup and first run

**Deployment status:** importable workflow prototype; live integration testing required.

## 1. Prerequisites

- An n8n instance with Microsoft Outlook Trigger, Microsoft Outlook, HTTP Request, Code, Crypto, Merge, Wait, AI Agent and Google Gemini Chat Model nodes. Imported versions of individual node types may require migration on a different n8n release.
- A test Microsoft Outlook mailbox and working Outlook OAuth2 credentials.
- A Google Gemini credential enabled in n8n with access to a compatible model. The exported model value is `models/gemini-1.5-flash` and may need updating to one available to your account.
- A VirusTotal API key and a plan **authorized for your use case**. The public API is *not* licensed for commercial products or services.
- A reporting email address and authorization to analyze and submit sample files and URLs.

## 2. Configure the environment

The checked-in workflow contains these n8n expressions:

```text
{{ $env.VIRUSTOTAL_API_KEY }}
{{ $env.SECURITY_REPORT_EMAIL }}
```

Self-hosted n8n example (illustrative; adjust for your deployment tool):

```bash
export VIRUSTOTAL_API_KEY='your_licensed_key_here'
export SECURITY_REPORT_EMAIL='security-reports@example.com'
# Launch/restart n8n using your normal method so these variables reach its process.
```

`N8N_BLOCK_ENV_ACCESS_IN_NODE=true` prevents `$env` expressions from reading variables. A hardened or n8n Cloud instance may not allow this approach. In that case, **do not disable security settings without review**: instead, configure VirusTotal API credentials in n8n's credential store (for example HTTP Header Auth with `x-apikey`) and adjust all VirusTotal HTTP nodes to use them. Store the report destination in a safe authorized configuration. Avoid passing a secret key through the **Set** node because it may appear in execution data. See [n8n security environment variables](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/security).

`.env.example` is documentation, not a file that n8n automatically loads. Do not commit real environment files or keys.

## 3. Import the JSON

1. Open n8n and create a workflow.
2. Use the workflow menu's **Import from File** command and select `security-analyst-workflow.json`.
3. Review connections, warnings, and any node migration prompts.
4. Save without activating the trigger yet.

See [n8n export/import documentation](https://docs.n8n.io/build/manage-workflows/export-and-import).

## 4. Connect credentials

Assign Outlook OAuth2 credentials to **On New Email**, **Get Attachments List**, **Download Attachment**, and **Send Security Report Email**. Assign your Google Gemini credential to **Google Gemini**. The supplied JSON contains only placeholder credential identifiers; it will not authenticate automatically.

Review OAuth scopes and avoid unnecessary mailbox-wide privileges. Make sure the recipient can accept the reports and that the sender filter prevents mail loops.

## 5. Verify before activation

- Confirm the report recipient; do not accidentally send security data to a shared or external mailbox.
- Confirm VirusTotal endpoint permissions and upload policy. The workflow **automatically submits attachments** through the standard file endpoint; it does not ask for per-file consent.
- Remember that URL and attachment scans currently run through separate branches. Analyze one message at a time while testing; join/metadata mapping needs further QA.
- The Wait node uses a fixed **15-second** delay; this is not an analysis-completion guarantee.
- If a VirusTotal request fails or returns pending, treat the outcome as **inconclusive**. No alert should be treated as a clean bill of health.
- Ensure your API quota covers the number of extracted URLs plus file hash checks, uploads, and result queries.

## 6. Safe end-to-end test plan

Use a dedicated mailbox with synthetic messages; do not send malware or sensitive personal data.

| Test | Expected behavior to verify |
| --- | --- |
| No URLs, no attachments | A no-scannable-indicators notice, **not** a clean verdict |
| One harmless URL | Submission and a readable HTML result, or explicit pending/error state |
| One dummy text attachment | Hash, file workflow and a final result; verify external upload authorization |
| Two URL candidates | Separate requests, correct result association and quota behavior |
| URL + dummy attachment | Both branches complete and report aggregates without lost/mislabelled evidence |
| Invalid API key or quota exceeded | Error is visible and **not** reported as clean |
| Processing still pending after 15s | Report remains **inconclusive** |
| Message from report mailbox | No self-trigger loop |

Record the observed n8n version, screenshots and test results before calling this production ready.

## 7. Runtime troubleshooting

**Missing credentials:** reselect each Outlook/Gemini credential after import.

**`access to env vars denied`:** follow section 2 and use n8n-managed credentials instead of unblocking secrets indiscriminately.

**VirusTotal 401 / 403:** check token permissions and account/plan; don't expose the key in issue screenshots.

**VirusTotal 429:** respect rate limits, use queueing/backoff and a licensed quota. The included workflow does not include full rate-limit handling.

**Unexpectedly missing attachment or filename:** inspect the attachment nodes and the `Aggregate Scan Results` mapping. Matching by order is a known limitation.

**No final report:** inspect execution history and Merge node inputs. Branch synchronization and API failure handling are not yet hardened.
