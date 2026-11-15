# Contributing

Thanks for your interest in improving the n8n Security Analyst Agent.

This repository is **all rights reserved**, not an open-source-licensed project. Contact the maintainer before reusing or redistributing contributions. By proposing changes, you confirm that you have the rights to contribute them. Submission alone does not confer an outbound license.

## Development

1. Work in a feature branch and describe the problem being solved.
2. Do not include real emails, API keys, OAuth tokens, customer data, or unredacted logs.
3. Run `python scripts/validate_workflow.py` and `python -m unittest discover -s tests -v`.
4. For workflow changes, include n8n version, screenshots with sensitive data redacted, and manual test steps.
5. Open a pull request with a description of changes, potential security impacts, and test evidence.

## Guidelines

- Favor small, reviewable changes that preserve importability.
- Do not disable TLS verification, silence scan errors, or report pending as clean.
- Never send sensitive attachments to an external scanner without explicit authorization.
- Treat inbound email content as untrusted data; avoid blindly rendering it as HTML.
- Use placeholders and mocked inputs in tests.

**Security reports:** follow [SECURITY.md](SECURITY.md) rather than publishing exploit details in an issue.
