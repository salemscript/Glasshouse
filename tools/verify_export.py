#!/usr/bin/env python3
"""Check the complete static export without dependencies or a network connection."""
import gzip
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
MANIFEST = ROOT / 'EXPORT-MANIFEST.json'

def inventory():
    result = []
    for p in sorted(SITE.rglob('*')):
        if p.is_symlink():
            raise ValueError(f'Unexpected symbolic link: {p}')
        if not p.is_file():
            continue
        data = p.read_bytes()
        result.append({'path': p.relative_to(SITE).as_posix(),
                       'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return result

def check_link(source, value):
    value = value.strip()
    url = urlsplit(value)
    if not value or value.startswith('#') or url.scheme or url.netloc:
        return
    if value.startswith('/'):
        raise ValueError(f'Root-relative reference may break project Pages: {source.name}: {value}')
    target = (source.parent / unquote(url.path)).resolve()
    if not target.is_relative_to(SITE.resolve()):
        raise ValueError(f'Reference leaves website folder: {source.name}: {value}')
    if url.path and not target.exists():
        raise ValueError(f'Missing local asset: {source.relative_to(SITE)}: {value}')

class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.source = source
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ('src', 'href'):
            if name in attrs:
                check_link(self.source, attrs[name])

def main():
    manifest = json.loads(MANIFEST.read_text())
    current = inventory()
    if sys.argv[1:] == ['--refresh']:
        manifest['files'] = current
        manifest['totalWebsiteBytes'] = sum(p['bytes'] for p in current)
        manifest['fileCount'] = len(current)
        manifest['note'] = 'Manifest refreshed locally; website may differ from original source snapshot.'
        MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
        print('Manifest refreshed. Run this check again before publishing.')
        return
    if sys.argv[1:]:
        raise ValueError('Use no arguments to verify, or --refresh after intentional edits.')
    if not (SITE / 'index.html').is_file():
        raise ValueError('Missing site/index.html; keep the extracted folder structure.')
    if current != manifest['files']:
        old = {p['path']: p for p in manifest['files']}
        new = {p['path']: p for p in current}
        changed = sorted(p for p in old.keys() | new.keys() if old.get(p) != new.get(p))
        raise ValueError('Manifest mismatch: ' + ', '.join(changed[:10]))
    if sum(p['bytes'] for p in current) >= 1_000_000_000:
        raise ValueError('Website exceeds the 1 GB Pages site limit.')
    if any(p['bytes'] > 100 * 1024 * 1024 for p in current):
        raise ValueError('An individual file exceeds the regular GitHub file limit.')
    compressed = 0
    for p in SITE.rglob('*.json.gz'):
        json.loads(gzip.decompress(p.read_bytes()))
        compressed += 1
    for p in SITE.rglob('*.html'):
        Links(p).feed(p.read_text())
    for p in SITE.rglob('*.css'):
        for match in re.finditer(r'url\(\s*[\"\x27]?([^\)\"\x27]+)', p.read_text()):
            check_link(p, match.group(1))
    print(f'PASS: {len(current)} website files, '
          f'{sum(p["bytes"] for p in current):,} bytes, '
          f'{compressed} compressed JSON files; hashes and local references verified.')

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        print(f'Export check failed: {error}', file=sys.stderr)
        sys.exit(1)
