# Changelog

## Unreleased — repository professionalization

### Added
- Usage, architecture, security, licensing and marketplace documentation
- Agensi-compatible skill scaffold and local packaging tool
- Offline JSON validation, unit tests and GitHub Actions CI
- Contribution, issue, pull request, and security report templates

### Security changes
- Removed the `allowUnauthorizedCerts` override from the VirusTotal hash lookup node
- Replaced inline VirusTotal key and reporting email placeholders with self-hosted n8n environment references
- Removed an unused empty HTTP header and unresolved generic credential choice from the URL submission node
- Reworded the no-indicator and AI summaries to avoid presenting absence of detections as proof of safety

### Still required
- Live integration and failure-mode testing
- API quota / licensing validation
- Explicit privacy consent and attachment upload policy
- Robust asynchronous polling, evidence mapping, and escalation design
