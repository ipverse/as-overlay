#!/usr/bin/env python3
"""Validate overlay.json structure and data quality."""

import json
import sys
from pathlib import Path

import pycountry

VALID_COUNTRY_CODES = {country.alpha_2 for country in pycountry.countries}

VALID_REASONS = {'missing', 'correction'}

# ASN validation ranges
MAX_ASN = 4294967295  # 2^32 - 1
RESERVED_ASNS = {0, 23456, 65535, 4294967295}
RESERVED_ASN_RANGES = [(65536, 65551)]  # Documentation/sample code
PRIVATE_ASN_RANGES = [(64512, 65534), (4200000000, 4294967294)]

# Field length limits
MAX_HANDLE_LENGTH = 30
MAX_DESCRIPTION_LENGTH = 100


def is_asn_in_ranges(asn, ranges):
    """Check if ASN is in any of the given ranges."""
    return any(start <= asn <= end for start, end in ranges)


def validate_overlay():
  """Validate overlay.json file."""
  errors = []
  warnings = []

  # Load JSON
  overlay_path = Path('overlay.json')
  if not overlay_path.exists():
    print(f"Error: {overlay_path} not found")
    return False

  # Read file to calculate line numbers
  try:
    with open(overlay_path, 'r', encoding='utf-8') as f:
      file_lines = f.readlines()
  except Exception as e:
    print(f"Error reading file: {e}")
    return False

  try:
    with open(overlay_path, 'r', encoding='utf-8') as f:
      data = json.load(f)
  except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON syntax: {e}")
    return False

  # Check it's an array
  if not isinstance(data, list):
    errors.append("overlay.json must contain a JSON array")
    print('\n'.join(errors))
    return False

  # Calculate line number for each entry in the JSON array
  def get_line_number(entry_idx):
    """Find the line number where an entry starts in the file."""
    asn_count = 0
    for line_num, line in enumerate(file_lines, 1):
      if '"asn"' in line:
        if asn_count == entry_idx:
          return line_num
        asn_count += 1
    return entry_idx + 2  # Fallback: approximate

  # Track ASNs to check for duplicates
  seen_asns = set()
  previous_asn = None

  for idx, entry in enumerate(data):
    entry_num = idx + 1
    line = get_line_number(idx)

    # Check required fields
    if 'asn' not in entry:
      errors.append(f"Line {line}: Missing required field 'asn'")
      continue

    asn = entry.get('asn')

    # Validate ASN type first so we can use it in error messages
    if not isinstance(asn, int) or asn <= 0:
      errors.append(f"Line {line}: ASN must be a positive integer, got {asn}")
      continue

    if 'reason' not in entry:
      errors.append(f"Line {line} (AS{asn}): Missing required field 'reason'")

    if 'countryCode' not in entry:
      errors.append(f"Line {line} (AS{asn}): Missing required field 'countryCode'")

    # Validate ASN range
    if asn > MAX_ASN:
      errors.append(f"Line {line} (AS{asn}): ASN exceeds maximum value ({MAX_ASN})")
      continue

    # Check for reserved ASNs
    if asn in RESERVED_ASNS:
      errors.append(f"Line {line} (AS{asn}): Reserved ASN cannot be used")
      continue

    if is_asn_in_ranges(asn, RESERVED_ASN_RANGES):
      errors.append(f"Line {line} (AS{asn}): Reserved ASN range (documentation/sample code)")
      continue

    # Warn about private ASNs
    if is_asn_in_ranges(asn, PRIVATE_ASN_RANGES):
      warnings.append(f"Line {line} (AS{asn}): Private ASN - verify it's actually announcing prefixes publicly")

    # Check for duplicates
    if asn in seen_asns:
      errors.append(f"Line {line}: Duplicate ASN {asn}")
    seen_asns.add(asn)

    # Check sorting
    if previous_asn is not None and asn < previous_asn:
      errors.append(f"Line {line}: ASNs must be sorted (ASN {asn} comes after {previous_asn})")
    previous_asn = asn

    # Validate reason
    reason = entry.get('reason')
    if reason and reason not in VALID_REASONS:
      errors.append(f"Line {line} (AS{asn}): Invalid reason '{reason}', must be 'missing' or 'correction'")

    # Validate country code if present
    country_code = entry.get('countryCode')
    if country_code:
      if not isinstance(country_code, str) or len(country_code) != 2:
        errors.append(f"Line {line} (AS{asn}): Country code must be a 2-letter ISO 3166-1 alpha-2 code")
      elif country_code not in VALID_COUNTRY_CODES:
        errors.append(
          f"Line {line} (AS{asn}): Invalid country code '{country_code}' (must be valid ISO 3166-1 alpha-2)")

    # Validate handle and description are together
    has_handle = 'handle' in entry and entry['handle']
    has_description = 'description' in entry and entry['description']

    if has_handle and not has_description:
      errors.append(f"Line {line} (AS{asn}): 'handle' provided without 'description' (must be together)")
    if has_description and not has_handle:
      errors.append(f"Line {line} (AS{asn}): 'description' provided without 'handle' (must be together)")

    # Validate handle format if present
    handle = entry.get('handle')
    if handle:
      if not isinstance(handle, str):
        errors.append(f"Line {line} (AS{asn}): 'handle' must be a string")
      elif ' ' in handle:
        errors.append(f"Line {line} (AS{asn}): 'handle' should not contain spaces")
      elif handle != handle.upper():
        warnings.append(f"Line {line} (AS{asn}): 'handle' should be uppercase (got '{handle}')")
      elif len(handle) > MAX_HANDLE_LENGTH:
        errors.append(f"Line {line} (AS{asn}): 'handle' too long ({len(handle)} chars, max {MAX_HANDLE_LENGTH})")

    # Validate description length if present
    description = entry.get('description')
    if description:
      if not isinstance(description, str):
        errors.append(f"Line {line} (AS{asn}): 'description' must be a string")
      elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(f"Line {line} (AS{asn}): 'description' too long ({len(description)} chars, max {MAX_DESCRIPTION_LENGTH})")

    # Semantic validation: if only countryCode provided (no handle/description), reason should be "missing"
    if country_code and not has_handle and reason == 'correction':
      errors.append(f"Line {line} (AS{asn}): Cannot use reason='correction' for country-only overlay (use 'missing')")

    # Check for unexpected fields
    expected_fields = {'asn', 'reason', 'handle', 'description', 'countryCode'}
    unexpected = set(entry.keys()) - expected_fields
    if unexpected:
      warnings.append(f"Line {line} (AS{asn}): Unexpected fields: {', '.join(unexpected)}")

    # Check field order: asn, handle, description, countryCode, reason
    expected_order = ['asn', 'handle', 'description', 'countryCode', 'reason']
    actual_keys = list(entry.keys())
    # Filter expected_order to only include fields that are present
    expected_present = [k for k in expected_order if k in actual_keys]
    if actual_keys != expected_present:
      errors.append(f"Line {line} (AS{asn}): Incorrect field order. Expected: {', '.join(expected_present)}, got: {', '.join(actual_keys)}")

  # Print results
  if errors:
    print("ERRORS:")
    for error in errors:
      print(f"  ✗ {error}")
    print()

  if warnings:
    print("WARNINGS:")
    for warning in warnings:
      print(f"  ⚠ {warning}")
    print()

  if not errors and not warnings:
    print(f"✓ All {len(data)} entries are valid")
    return True
  elif not errors:
    print(f"✓ All {len(data)} entries are valid (with {len(warnings)} warnings)")
    return True
  else:
    print(f"✗ Validation failed with {len(errors)} error(s) and {len(warnings)} warning(s)")
    return False


if __name__ == '__main__':
  success = validate_overlay()
  sys.exit(0 if success else 1)
