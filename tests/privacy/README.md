# Privacy Hook Tests

Pytest suite for `hooks/check_counselor_privacy.py`. Each test invokes the
hook as a subprocess so the tests exercise the same entry point Claude Code
calls.

## Run

```bash
pip install pytest
pytest tests/privacy
```

Python 3.8+ and pytest are the only dependencies.

## Coverage

| Test | What it verifies |
|------|------------------|
| `test_clean_counselor_report_passes` | A counselor report with no flagged terms exits 0. |
| `test_counselor_report_with_fafsa_warns` | FAFSA + EFC in a counselor report exits 2 with both terms in stderr. |
| `test_keyword_match_is_case_insensitive` | Lowercase "snap" matches the configured "SNAP" keyword. |
| `test_private_supplement_is_ignored` | Financial terms in the private supplement are allowed. |
| `test_non_counselor_report_is_ignored` | Writes to unrelated files are not inspected. |
| `test_malformed_payload_does_not_block` | A bad JSON payload exits 0 (never blocks Claude). |
| `test_edit_reads_file_from_disk` | Edit triggers the hook and reads post-edit content from disk. |
| `test_multiedit_reads_file_from_disk` | MultiEdit follows the same on-disk read path. |
| `test_edit_clean_file_passes` | Edits to clean reports exit 0. |
| `test_keyword_config_drives_matching` | Removing keywords from the JSON config disables those matches. |

## Adding a keyword

Edit `hooks/private-keywords.json`. Add a fixture under `fixtures/` and a
test function in `test_privacy_hook.py` that asserts the new term warns
in a counselor report.
