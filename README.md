# Autonomous System Metadata Overlay

Community-maintained metadata for autonomous systems with missing or incorrect WHOIS data.

## 🔍 See it in action

Explore how overlay data enriches AS metadata at **[Lens by ipverse](https://lens.ipverse.net)**.

## What is this?

Sometimes an AS is announcing prefixes but has:
- No WHOIS records
- Missing country codes in WHOIS
- Incorrect inferred metadata

This overlay fills those gaps and is automatically imported into [ipverse](https://github.com/ipverse).

## How it works

When WHOIS data is missing, ipverse uses inference to discover metadata automatically. When that inference is wrong or incomplete, this overlay provides corrections. Once authoritative WHOIS records appear, overlay entries are typically removed.

## Missing metadata

The file `missing.json` lists autonomous systems with incomplete metadata. Each entry has a `missing` field indicating what's missing:

- `"all"` - Autonomous systems with no metadata at all
- `"country"` - Autonomous systems with metadata but missing country code

This file is auto-generated. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to use it.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- How to add entries
- Research ideas
- Example pull request descriptions
- Contribution license terms (CC0 1.0)

## Questions or issues?

Head over to the [feedback repository](https://github.com/ipverse/feedback) if you have questions, issues, or suggestions.

## License

This data is released under [CC0 1.0 Universal](LICENSE).
