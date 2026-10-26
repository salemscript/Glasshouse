"""Check chapter counts, source dependencies, and glyph boundaries for the import."""
import fitz,gzip,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=(root/'site/linear-review-data.js').read_text()
qs=json.loads(source.split('=',1)[1].strip().removesuffix(';'))
starts=[1,118,146,202,291,341,399,446,509]
counts=[29,37,25,18,20,21,15,26,14]
assert len(qs)==205
ids={q['id'] for q in qs};assert len(ids)==205
for ch,count in enumerate(counts,1):
 rows=[q for q in qs if q['chapter']==ch]
 assert [q['number'] for q in rows]==list(map(str,range(1,count+1)))
 doc=fitz.open(root/f'site/books/linear-algebra/chapter-{ch:02}.pdf')
 for q in rows:
  assert not q['grader'] and not q['steps']
  for ref in q.get('relatedQuestions',[]):assert ref in ids
  assert q['parts']
  for part in q['parts']:
   assert gzip.decompress((root/'site'/part['file']).read_bytes()).startswith(b'<svg')
   page=doc[part['pdfPage']-14-starts[ch-1]]
   for x,y,w,h in part['crops']:
    assert 0<=x<x+w<=page.rect.width and 0<=y<y+h<=page.rect.height
    cut=[word[4] for word in page.get_text('words') if word[0]<x+w-2 and word[2]>x+2 and ((word[1]<y<word[3]-.3) or (word[1]+.3<y+h<word[3]))]
    assert not cut,(q['id'],part['role'],cut)
print('PASS: all 205 questions, 9 complete number sequences, source files, references and vertical glyph boundaries.')
