# AGENTS.md

Guidelines for AI coding agents working in this repository.

## Overview

Community-maintained metadata overlay for autonomous systems with missing or
incorrect WHOIS data. Contributors add entries to correct or supplement AS
metadata that is missing from authoritative sources.

**Master Project:** `ipverse-java` (private repository)

## Files

| File | Editable | Description |
|------|----------|-------------|
| `overlay.json` | **Yes** | Manual corrections - the only data file to modify |
| `missing.json` | No | Auto-generated list of AS needing data |
| `CONTRIBUTING.md` | Reference | Contribution guidelines and license terms |

## Rules for AI Agents

1. **Only modify `overlay.json`** - never edit `missing.json` (it's auto-generated)
2. Follow exact field order: `asn`, `handle`, `description`, `countryCode`, `reason`
3. Entries must be sorted by ASN (ascending)
4. `handle` and `description` must appear together or not at all
5. Valid reasons: `missing` (adding new data) or `correction` (fixing inferred data)
6. Country codes must be valid ISO 3166-1 alpha-2

## Entry Format

Full metadata entry:
```json
{
  "asn": 64512,
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "missing"
}
```

Country-only entry:
```json
{
  "asn": 64512,
  "countryCode": "US",
  "reason": "missing"
}
```

## Validation

Run before committing:

```bash
pip install pycountry
python scripts/validate.py
```

GitHub Actions automatically validates PRs.

## Related Repositories (GitHub)

- `as-metadata` - ASN metadata exports (CSV/JSON)
- `as-ip-blocks` - Per-AS prefix data
- `country-ip-blocks` - Per-country prefix data

## Contributing

See `CONTRIBUTING.md` for detailed guidelines including:
- Where to find authoritative data sources
- PR description requirements
- License terms (CC0 1.0 Universal)
