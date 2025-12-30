# Autonomous System Metadata Overlay

Sometimes autonomous systems (AS) are announcing prefixes but have no WHOIS records, or WHOIS records have missing countries. The `overlay.json` fills those gaps. This is a community-maintained file - contributions are welcome.

For AS without WHOIS records, an inference mechanism is used to discover metadata automatically. When that inference is wrong, you can correct it here. Don't override handle/description from WHOIS records (origin: `authoritative`) - only add missing data or fix inferred metadata. See examples below.

**Note:** When a WHOIS record appears for an AS, any overlay entry with metadata for that AS will be removed since the authoritative source now exists.

## Structure

Each entry has the following fields:

```json
{
  "asn": 64512,
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "missing"
}
```

### Fields

Fields must appear in this exact order:

- `asn` (required) - The AS number
- `handle` (optional, but must be paired with `description`) - AS handle/name (uppercase, no spaces, keep it short)
- `description` (optional, but must be paired with `handle`) - Network description
- `countryCode` (required) - ISO 3166-1 alpha-2 country code
- `reason` (required) - Why this overlay exists (must be either `missing` or `correction`):
  - `missing` - Adding metadata that's missing (e.g., just country code, or completely missing metadata)
  - `correction` - Fixing mistakes in inferred metadata (never use this for authoritative metadata)

### Valid combinations

You can overlay:
1. Country code only (for AS with metadata but missing country)
2. Handle, description, and country code (for complete metadata)

**Note:** Country code is always required. Handle and description must be specified together - you can't have one without the other. Fields must appear in the order shown above.

## When to add entries

**Country code is null** (origin: `authoritative`):
```json
{
  "asn": 64512,
  "countryCode": "US",
  "reason": "missing"
}
```

**Missing metadata** (origin: `none`):
```json
{
  "asn": 64512,
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "missing"
}
```

**Inferred metadata is wrong** (origin: `inferred`):
```json
{
  "asn": 64512,
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "correction"
}
```

**Never do this:**
- Change handle/description with origin: `authoritative`
- Add entries based on personal naming preferences
- Add AS that aren't announcing prefixes

## Contributing

When adding new entries:
1. Always include a `reason` field
2. Include sources in your PR description showing where you got the information:
   - IRR databases (RADb, RIPE, AFRINIC, etc.)
   - PeeringDB entries
   - BGP looking glass data (Hurricane Electric, RouteViews)
   - RIR stats and lookup tools (RIPE Stat, ARIN's ASN lookup)
3. Keep descriptions concise and factual
4. Keep PRs small - each entry is reviewed manually, so submit just a few entries at a time

### Validation

Before submitting, you can validate your changes locally:

```bash
# Install dependencies
pip install pycountry

# Validate your changes
python scripts/validate.py
```

All pull requests are automatically validated via GitHub Actions.

Example PR description:
```
Adding AS64512 - missing from WHOIS but actively announcing prefixes

Active announcements: https://github.com/example/ipverse-data/blob/main/as.csv shows AS64512
IRR: RADb shows aut-num AS64512 with descr "Acme Corporation"
PeeringDB: https://www.peeringdb.com/asn/64512 confirms US location
```

## License

This dataset is dedicated to the public domain under [CC0 1.0 Universal](LICENSE). You can copy, modify, and distribute the data, even for commercial purposes, without asking permission.
