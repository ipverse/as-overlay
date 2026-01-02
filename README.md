# Autonomous System Metadata Overlay

Community-maintained metadata for autonomous systems with missing or incorrect WHOIS data.

## What is this?

Sometimes AS are announcing prefixes but have:
- No WHOIS records
- Missing country codes in WHOIS
- Incorrect inferred metadata

This overlay fills those gaps and is automatically imported into [ipverse](https://github.com/ipverse).

## How it works

When WHOIS data is missing, ipverse uses inference to discover metadata automatically. When that inference is wrong or incomplete, this overlay provides corrections. Once authoritative WHOIS records appear, overlay entries are typically removed

## Missing data

The file `missing.json` lists AS with incomplete data. Each entry has a `missing` field indicating what's missing:

- `"all"` - AS with no metadata at all
- `"country"` - AS with metadata but missing country code

This file is auto-generated. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to use it.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Contribution license terms (CC0 1.0)
- How to add entries
- Validation instructions
- Example pull request descriptions

## Questions or issues?

Head over to the [feedback repo](https://github.com/ipverse/feedback) if you have questions, issues, or suggestions.

## License

This data is released under [CC0 1.0 Universal](LICENSE).
