# Contributing to as-overlay

Great, you want to contribute! Here's how:

**Keep PRs small** - Each entry is reviewed manually, so submit only a handful of entries at a time.

## Contribution workflow

1. **Find an AS** - Browse `missing.json` to find an AS that needs data
2. **Research** - Look up the AS using primary sources (see [Where to find data](#where-to-find-data))
3. **Add entry** - Create an entry in `overlay.json` with the data found
4. **Validate** - Run the validation script locally to check formatting
5. **Submit PR** - Open a pull request with sources documented (see [PR description requirements](#pr-description-requirements))

## Finding AS to work on

The auto-generated file `missing.json` lists AS that need overlay entries:

```json
{
  "as": [
    { "asn": 11636, "missing": "all" },
    { "asn": 58531, "missing": "country" }
  ]
}
```

The `missing` field indicates what's missing:

- `"all"` - No metadata at all. These need complete metadata (handle, description, and country code).
- `"country"` - Has metadata but missing country code. These only need a country code added.

**Note**: This file is auto-generated. Do not include it in your PR - only `overlay.json` should be modified.

## Entry structure

Each entry in `overlay.json` follows one of two formats. For full metadata (when `"missing": "all"` or for corrections):

```json
{
  "asn": 64512,
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "missing"
}
```

For country code only (when `"missing": "country"`):

```json
{
  "asn": 64512,
  "countryCode": "US",
  "reason": "missing"
}
```

### Field definitions

Fields must appear in this exact order:

| Field | Required | Description |
|-------|----------|-------------|
| `asn` | Yes | The AS number |
| `handle` | No* | AS handle/name (uppercase, no spaces, keep it short) |
| `description` | No* | Network description (concise and factual) |
| `countryCode` | Yes | ISO 3166-1 alpha-2 country code |
| `reason` | Yes | `missing` (adding data that doesn't exist) or `correction` (fixing inferred metadata - never for authoritative data) |

*Handle and description must be specified together - one cannot appear without the other.

## Validation

### Where to find data

- IRR databases (RADb, RIPE, AFRINIC, etc.)
- PeeringDB
- BGP looking glasses (Hurricane Electric, RouteViews)
- BGP AS path analysis (inferring location from upstream/peer relationships)

**Important**: Avoid citing ASN lookup aggregators (bgp.he.net, ipinfo.io, Team Cymru, etc.) - use primary sources instead.

### Local validation

```bash
# Install dependencies
pip install pycountry

# Validate changes
python scripts/validate.py
```

All pull requests are automatically validated via GitHub Actions.

### PR description requirements

Include sources showing where the data was obtained.

## Examples

### Full metadata

For an AS with `"missing": "all"` (no metadata at all):

```json
{
  "asn": 64512,
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "missing"
}
```

### Correction

For an AS with incorrect **inferred** metadata:

```json
{
  "asn": 64512,
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "correction"
}
```

### Country code only

For an AS with `"missing": "country"` (has metadata, missing country):

```json
{
  "asn": 64512,
  "countryCode": "US",
  "reason": "missing"
}
```

### Example PR description

```
Adding AS64512 - missing from WHOIS but actively announcing prefixes

Active announcements: https://github.com/example/ipverse-data/blob/main/as.csv shows AS64512
IRR: RADb shows aut-num AS64512 with descr "Acme Corporation"
PeeringDB: https://www.peeringdb.com/asn/64512 confirms US location
```

### What NOT to do

- Change handle/description when origin is `authoritative` - only overlay missing or inferred data
- Add entries based on personal naming preferences
- Add AS that are not announcing prefixes
- Use `correction` for authoritative metadata

## Questions or issues?

If you have questions about contributing or the license terms, please head over to the [feedback repo](https://github.com/ipverse/feedback).

---

## License agreement

**By contributing to this project, you agree to release your contribution under the [CC0 1.0 Universal](LICENSE) license.**

### What does this mean?

CC0 1.0 Universal is a public domain dedication. When you contribute:

- You waive all copyright and related rights to your contribution
- Your contribution becomes part of the public domain
- Anyone can use, modify, and distribute your contribution without restriction
- No attribution is required (though sources should still be documented in PRs)

This ensures the data remains freely available for everyone to use without legal restrictions.

### Why CC0?

CC0 is used because factual AS metadata should be freely accessible to the entire internet community. This license:

- Removes all legal barriers to using the data
- Allows unrestricted commercial and non-commercial use
- Ensures the data can be integrated into any system or database
- Is standard practice for public infrastructure data projects

## Contributor affirmations

By submitting a contribution, you affirm that:

- **You have the right to contribute the data** - The information you're submitting is either publicly available, factual data that you have the right to share
- **The data is factual and publicly verifiable** - AS metadata should be based on public sources like IRR databases, PeeringDB, BGP looking glasses, and RIR records
- **You're not submitting proprietary or confidential information** - Only contribute data that is publicly available or can be publicly verified
