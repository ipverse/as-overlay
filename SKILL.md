---
name: research-missing-as
description: Research a missing AS entry for overlay.json. Investigates BGP announcements, prefix ownership, and AS paths to identify organization and country. Invoke with /research-missing-as {ASN}
---

# Research Missing AS

## Background

An AS (Autonomous System) is a network or collection of networks under a single administrative entity, identified by a unique ASN (Autonomous System Number). ASes exchange routing information via BGP (Border Gateway Protocol) to enable internet traffic to flow between networks. Each AS announces IP prefixes (address blocks) it controls to its BGP peers.

AS metadata (organization name, country, handle) is typically published in RIR (Regional Internet Registry) databases. However, some ASes actively announce prefixes via BGP without publishing proper WHOIS metadata - these are the entries we need to research.

## Your Role

You are a community contributor researching an AS entry to add to `overlay.json`. Your goal is to find the organization name and country for an AS that has actively announced BGP prefixes but no published metadata.

**Important**: Research only ONE AS at a time. Each PR should contain data for a single AS only. Do not submit another PR until the previous one has been merged.

## Instructions

### Step 1: Parse and Validate

Extract the ASN from the user's argument (e.g., `/research-missing-as 11636` means ASN 11636).

Read `missing.json` and verify:
- The ASN exists in the file
- The entry has `"missing": "all"`

If the ASN is not found or has `"missing": "country"`, inform the user and stop.

### Step 2: Initial Discovery

Fetch data from primary sources in parallel:

1. **PeeringDB** - `https://www.peeringdb.com/asn/{ASN}`
   - Look for: organization name, country, network type

2. **BGP.HE.NET** - `https://bgp.he.net/AS{ASN}`
   - Look for: announced prefixes, upstream ASes, peer ASes, any descriptive text
   - Note the list of IPv4/IPv6 prefixes being announced

Record all findings. If PeeringDB has complete data, you may have enough already.

### Step 3: Prefix Ownership Investigation

For the announced prefixes found in Step 2, trace their allocation:

1. Identify which RIR allocated the prefix based on the IP range:
   - **ARIN** (North America): Use `https://rdap.arin.net/registry/ip/{prefix}`
   - **RIPE** (Europe/Middle East/Central Asia): Use `https://rdap.db.ripe.net/ip/{prefix}`
   - **APNIC** (Asia Pacific): Use `https://rdap.apnic.net/ip/{prefix}`
   - **LACNIC** (Latin America/Caribbean): Use `https://rdap.lacnic.net/rdap/ip/{prefix}`
   - **AFRINIC** (Africa): Use `https://rdap.afrinic.net/rdap/ip/{prefix}`

2. Query the appropriate RIR's RDAP endpoint for each prefix

3. Record:
   - Organization name from allocation record
   - Country code from allocation record
   - Any handle/identifier

The organization that paid the RIR for the prefix allocation is often the AS operator.

### Step 4: AS Path Analysis

If the country is still unclear after Steps 2-3, analyze BGP relationships:

1. From BGP.HE.NET, identify the upstream providers
2. Research where those upstreams operate:
   - If all upstreams are regional ISPs in one country, the AS is likely there
   - Example: All upstreams are South African ISPs = AS is likely in ZA
3. Check peer relationships for additional geographic clues

### Step 5: Synthesize Findings

Based on all gathered evidence:

1. **Determine organization name**: Use the most authoritative source (RIR allocation > PeeringDB > BGP description)

2. **Determine country code**: Must be ISO 3166-1 alpha-2 (e.g., US, DE, BR, ZA)
   - Cross-reference multiple sources for confidence
   - RIR allocation country is usually definitive

3. **Generate handle** if none was found:
   - Based on organization name
   - UPPERCASE
   - No spaces (use hyphens)
   - Keep it short (e.g., "Acme Corporation" → "ACME-NET" or "ACME-CORP")

### Step 6: Prepare Output

Format the overlay.json entry with fields in this exact order:

```json
{
  "asn": {ASN},
  "handle": "{HANDLE}",
  "description": "{Organization Name}",
  "countryCode": "{CC}",
  "reason": "missing"
}
```

Format the PR description:

```markdown
Adding AS{ASN} - missing from WHOIS but actively announcing prefixes

**Sources:**
- BGP.HE.NET: https://bgp.he.net/AS{ASN} shows active announcements
- PeeringDB: https://www.peeringdb.com/asn/{ASN} [findings]
- {RIR} RDAP: {prefix} allocated to {org} in {country}
- [Additional sources used]

**Evidence summary:**
- Organization: {how determined}
- Country: {how determined}
```

Present both the overlay.json entry and PR description to the user for review. Do NOT modify any files until the user approves.

## Data Freshness

Be mindful of stale data. AS metadata changes over time:
- Organizations get acquired or renamed
- Prefixes get reassigned to different entities
- Country registrations change when companies relocate

**Always prefer recent data:**
- Check dates on RIR records (look for "last modified" or "changed" fields)
- BGP.HE.NET shows when prefixes were first/last seen - prefer actively announced prefixes
- If PeeringDB data conflicts with recent RIR records, the RIR is likely more current
- Historical whois data may be outdated - cross-reference with current BGP state

**Red flags for stale data:**
- Prefix not currently announced (check BGP.HE.NET for "not announced" status)
- RIR record unchanged for many years while other sources show different info
- Organization name doesn't match current corporate records

When sources conflict, weight recent evidence more heavily than historical records.

## Data Sources

### Primary Sources (USE THESE)
- **PeeringDB**: https://www.peeringdb.com/asn/{ASN}
- **BGP.HE.NET**: https://bgp.he.net/AS{ASN}
- **RIR RDAP endpoints** (see Step 3)
- **RADb/IRR**: Query via whois if needed

### DO NOT USE (Aggregators)
- ipinfo.io
- Team Cymru
- bgpview.io
- Other lookup aggregators

Per CONTRIBUTING.md, only primary sources should be cited in PRs.

## Entry Format Reference

Full metadata entry (for `missing: "all"`):
```json
{
  "asn": 64512,
  "handle": "ACME-NET",
  "description": "Acme Corporation",
  "countryCode": "US",
  "reason": "missing"
}
```

Field order is mandatory: `asn`, `handle`, `description`, `countryCode`, `reason`

## Validation

After preparing the entry, remind the user to run:
```bash
python scripts/validate.py
```

This validates the overlay.json format before committing.