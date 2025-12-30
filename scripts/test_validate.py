#!/usr/bin/env python3
"""Test suite for overlay.json validation."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

# Import the validation function
sys.path.insert(0, str(Path(__file__).parent))
from validate import validate_overlay


class TestValidation(unittest.TestCase):
    """Test cases for overlay.json validation."""

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()
        Path(self.test_dir).mkdir(exist_ok=True)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def write_overlay(self, data):
        """Write test overlay.json file."""
        overlay_path = Path(self.test_dir) / 'overlay.json'
        with open(overlay_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def run_validation(self):
        """Run validation in test directory."""
        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            return validate_overlay()
        finally:
            os.chdir(old_cwd)

    def test_valid_country_only_entry(self):
        """Test valid entry with only country code."""
        self.write_overlay([
            {
                "asn": 12345,
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        self.assertTrue(self.run_validation())

    def test_valid_complete_entry(self):
        """Test valid entry with all metadata."""
        self.write_overlay([
            {
                "asn": 12345,
                "handle": "ACME-NET",
                "description": "Acme Corporation",
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        self.assertTrue(self.run_validation())

    def test_missing_required_asn(self):
        """Test error when asn field is missing."""
        self.write_overlay([
            {
                "rir": "ARIN",
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_missing_required_reason(self):
        """Test error when reason field is missing."""
        self.write_overlay([
            {
                "asn": 12345,
                "countryCode": "US"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_invalid_country_code(self):
        """Test error for invalid country code."""
        self.write_overlay([
            {
                "asn": 12345,
                "countryCode": "XX",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_invalid_country_code_length(self):
        """Test error for wrong length country code."""
        self.write_overlay([
            {
                "asn": 12345,
                "countryCode": "USA",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_invalid_reason(self):
        """Test error for invalid reason value."""
        self.write_overlay([
            {
                "asn": 12345,
                "countryCode": "US",
                "reason": "invalid"
            }
        ])
        self.assertFalse(self.run_validation())


    def test_duplicate_asn(self):
        """Test error for duplicate ASN."""
        self.write_overlay([
            {
                "asn": 12345,
                "countryCode": "US",
                "reason": "missing"
            },
            {
                "asn": 12345,
                "countryCode": "GB",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_unsorted_asns(self):
        """Test error when ASNs are not sorted."""
        self.write_overlay([
            {
                "asn": 20000,
                "countryCode": "US",
                "reason": "missing"
            },
            {
                "asn": 10000,
                "countryCode": "GB",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_handle_without_description(self):
        """Test error when handle provided without description."""
        self.write_overlay([
            {
                "asn": 12345,
                "handle": "ACME-NET",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_description_without_handle(self):
        """Test error when description provided without handle."""
        self.write_overlay([
            {
                "asn": 12345,
                "description": "Acme Corporation",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_handle_with_spaces(self):
        """Test error when handle contains spaces."""
        self.write_overlay([
            {
                "asn": 12345,
                "handle": "ACME NET",
                "description": "Acme Corporation",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_handle_too_long(self):
        """Test error when handle exceeds max length."""
        self.write_overlay([
            {
                "asn": 12345,
                "handle": "A" * 31,
                "description": "Test",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_description_too_long(self):
        """Test error when description exceeds max length."""
        self.write_overlay([
            {
                "asn": 12345,
                "handle": "TEST",
                "description": "A" * 101,
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_entry_without_data(self):
        """Test error when entry has no country code or handle/description."""
        self.write_overlay([
            {
                "asn": 12345,
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_correction_reason_with_country_only(self):
        """Test error when using correction reason for country-only overlay."""
        self.write_overlay([
            {
                "asn": 12345,
                "countryCode": "US",
                "reason": "correction"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_reserved_asn_zero(self):
        """Test error for reserved ASN 0."""
        self.write_overlay([
            {
                "asn": 0,
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_reserved_asn_23456(self):
        """Test error for reserved ASN 23456."""
        self.write_overlay([
            {
                "asn": 23456,
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_reserved_asn_range(self):
        """Test error for reserved ASN range (documentation)."""
        self.write_overlay([
            {
                "asn": 65540,
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_asn_exceeds_max(self):
        """Test error for ASN exceeding maximum value."""
        self.write_overlay([
            {
                "asn": 4294967296,
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_negative_asn(self):
        """Test error for negative ASN."""
        self.write_overlay([
            {
                "asn": -1,
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        self.assertFalse(self.run_validation())

    def test_private_asn_warning(self):
        """Test warning for private ASN (should pass but warn)."""
        self.write_overlay([
            {
                "asn": 64512,
                "countryCode": "US",
                "reason": "missing"
            }
        ])
        # Should still pass validation (warning only)
        self.assertTrue(self.run_validation())


    def test_invalid_json(self):
        """Test error for invalid JSON syntax."""
        overlay_path = Path(self.test_dir) / 'overlay.json'
        with open(overlay_path, 'w') as f:
            f.write('{ invalid json }')
        self.assertFalse(self.run_validation())

    def test_not_array(self):
        """Test error when JSON is not an array."""
        self.write_overlay({"asn": 12345})
        self.assertFalse(self.run_validation())

    def test_multiple_valid_entries(self):
        """Test multiple valid entries in correct order."""
        self.write_overlay([
            {
                "asn": 1000,
                "countryCode": "US",
                "reason": "missing"
            },
            {
                "asn": 2000,
                "handle": "TEST-NET",
                "description": "Test Network",
                "countryCode": "GB",
                "reason": "correction"
            },
            {
                "asn": 3000,
                "handle": "SAMPLE-AS",
                "description": "Sample AS",
                "reason": "missing"
            }
        ])
        self.assertTrue(self.run_validation())


if __name__ == '__main__':
    unittest.main()
