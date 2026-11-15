# Security, privacy and responsible deployment

## Operating assumptions

This is a **proof of concept**, not a certified security product. Use a dedicated test mailbox and synthetic data first. The project owner or deployer is responsible for obtaining all required permissions for mailbox access, API use, storage, data transfer, and AI processing.

## Credential handling

- `VIRUSTOTAL_API_KEY` and `SECURITY_REPORT_EMAIL` are read via n8n expressions. No real key is bundled in the repository.
- Use n8n's credential manager for production-grade secret storage wherever possible. Environment variables are an optional self-hosted integration technique, not an alternative to access controls.
- Protect n8n's execution logs, database backups, environment configuration, and OAuth credential store.
- Limit OAuth permissions and rotate/revoke compromised credentials.
- Never post exports containing real account IDs, authorization headers, webhook URLs, credentials or execution pin data.
- TLS certificate verification must remain enabled. The original export had an `allowUnauthorizedCerts` setting; this version removes it.

## Data transfer and confidentiality

- URL submissions may expose private URL paths or query parameters.
- The existing attachment branch uploads full attachments to the **standard** VirusTotal file endpoint. **Do not send confidential files by default**. Plan for an explicit consent gate, classification checks, or a privacy-preserving authorized alternative before production.
- VirusTotal's **private scanning** is a distinct licensed service; the current workflow does not use it.
- Data passed to Google Gemini may include scan responses and attachment metadata. Review the model provider's policies and minimize personal information.
- Do not store full email body, security keys, or report data in permanent public artifacts.

## Supply-chain and licensing

VirusTotal explicitly restricts its **public** API to non-commercial use. A sellable integration or paid agent skill involving VirusTotal requires a permitted commercial arrangement and review of rate limits. Check provider terms directly; a marketplace listing does not grant third-party API rights.

## Common failure modes

- **Prompt injection:** emails and external API results are untrusted. Treat any embedded instructions as data and avoid model tool-use triggered by scan content.
- **HTML injection:** do not render raw email HTML into outgoing reports.
- **Incomplete verdicts:** no result, empty data, errors, or pending statuses are **unknown**, not clean.
- **False positives/negatives:** use human review and corroborating signals.
- **Mail loops and spam:** make sure reports do not repeatedly trigger the same workflow.
- **Rate limits / DoS:** one email may generate several API calls. Use quotas, timeouts and limited concurrency.
- **Cross-message mixups:** verify multi-message result association; do not claim strong per-item provenance from current aggregation code.

## Documentation sources

- [VirusTotal public API restrictions](https://docs.virustotal.com/reference/getting-started)
- [VirusTotal public vs. premium API](https://docs.virustotal.com/reference/public-vs-premium-api)
- [VirusTotal private file scanning](https://docs.virustotal.com/reference/private-files-api)
- [n8n environment-variable security](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/security)
