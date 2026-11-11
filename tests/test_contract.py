"""Document-contract checks only; no history, credentials or API access."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
REQUIRED = (
    '### 1. Inspect first',
    '### 2. Count real usage',
    '### 3. Rank and reconcile',
    '### 4. Choose the narrowest persistent writer',
    '### 5. Apply only the authorized change',
    '### 6. Readback is mandatory',
    'Inspection and ranking are read-only.',
    'A menu replacement requires explicit approval',
    'Keep raw history local.',
    'Deduplicate',
    'getMyCommands',
    'The approved ordered list is read back from the exact target',
)

def validate_contract(text):
    if len(text.encode('utf-8')) > 8192:
        raise ValueError('Skill exceeds the small-skill byte budget')
    if not text.startswith('---\n'):
        raise ValueError('Missing frontmatter')
    header = text.split('\n---\n', 1)[0]
    description = re.search(r'^description: (.+)$', header, re.MULTILINE)
    if not description or len(description[1]) > 60 or not description[1].endswith('.'):
        raise ValueError('Description must be a short trigger sentence')
    if 'name: hermes-test-commands' not in header:
        raise ValueError('Incorrect skill identity')
    for clause in REQUIRED:
        if clause not in text:
            raise ValueError('Missing required contract: ' + clause)

class SkillContractTests(unittest.TestCase):
    def test_small_valid_skill(self):
        validate_contract(SKILL)

    def test_inspection_only_is_read_only(self):
        self.assertIn('a request to inspect must not mutate the menu', SKILL)

    def test_ranked_update_has_safety_and_scope_contracts(self):
        for phrase in ['Verify sender identity per message', 'complete quoted-reply envelope', 'most recent invocation', 'explicit user exclusions', 'unrelated scopes remain unchanged']:
            self.assertIn(phrase, SKILL)

    def test_removal_preserves_remaining_order(self):
        self.assertIn('preserving the relative order of all others', SKILL)

    def test_missing_readback_contract_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_contract(SKILL.replace('### 6. Readback is mandatory', '### 6. Optional check'))

    def test_missing_authorization_contract_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_contract(SKILL.replace('A menu replacement requires explicit approval', 'Menus may be changed automatically'))

    def test_no_personal_operational_paths(self):
        for item in ['SKILL.md', 'README.md']:
            text = (ROOT / item).read_text(encoding='utf-8')
            self.assertNotRegex(text, r'/home/[^\s/]+/|/var/lib/|/etc/systemd/|\b\d{8,}:[A-Za-z0-9_-]{20,}')

if __name__ == '__main__':
    unittest.main()
