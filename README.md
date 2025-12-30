# Autonomous System Metadata Overlay

Sometimes autonomous systems (AS) are announcing prefixes but have no WHOIS records, or WHOIS records have missing countries. The `overlay.json` fills those gaps. This is a community-maintained file - contributions are welcome.

For AS without WHOIS records, an inference mechanism is used to discover metadata automatically. When that inference is wrong, you can correct it here. Don't override handle/description from WHOIS records (origin: `authoritative`) - only add missing data or fix inferred metadata. See examples below.

**Note:** When a WHOIS record appears for an AS, any overlay entry with metadata for that AS will be removed since the authoritative source now exists.

## Structure

Each entry has the following fields:

```json
{
  "asn": 12345,
  "rir": "ARIN",
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "missing"
}
```

### Fields

- `asn` (required) - The AS number
- `reason` (required) - Why this overlay exists (must be either `missing` or `correction`):
  - `missing` - Adding data that's null in WHOIS records (e.g., null country code, or completely missing AS metadata)
  - `correction` - Fixing mistakes in inferred metadata (never use this for authoritative WHOIS records)
- `rir` (optional) - Which RIR manages this AS
- `handle` (optional) - AS handle/name (uppercase, no spaces, keep it short)
- `description` (optional) - Network description
- `countryCode` (optional) - ISO 3166-1 alpha-2 country code

### Valid combinations

You can overlay:
1. Just the country code
2. Handle and description together (with or without country)

Handle and description must always be specified together - you can't have one without the other.

## When to add entries

**Country code is null** (origin: `authoritative`):
```json
{
  "asn": 12345,
  "countryCode": "US",
  "reason": "missing"
}
```

**Metadata is null** (no WHOIS record, AS is announcing prefixes):
```json
{
  "asn": 12345,
  "rir": "ARIN",
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "missing"
}
```

**Inferred metadata is wrong** (origin: `inferred`):
```json
{
  "asn": 12345,
  "rir": "ARIN",
  "handle": "ACME-NET",
  "description": "Acme Corporation",
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
3. Include the `rir` field if known
4. Keep descriptions concise and factual
5. Keep PRs small - each entry is reviewed manually, so submit just a few entries at a time

Example PR description:
```
Adding AS64512 - missing from WHOIS but actively announcing prefixes

Active announcements: https://github.com/example/ipverse-data/blob/main/as.csv shows AS64512
IRR: RADb shows aut-num AS64512 with descr "Acme Corporation"
PeeringDB: https://www.peeringdb.com/asn/64512 confirms US location
```

## License

This dataset is dedicated to the public domain under [CC0 1.0 Universal](LICENSE). You can copy, modify, and distribute the data, even for commercial purposes, without asking permission.
