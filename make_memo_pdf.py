"""Make a portable, two-page plain-text PDF of MEMO.md without dependencies."""
import re
import textwrap
from pathlib import Path

root = Path(__file__).resolve().parent
text = (root / 'MEMO.md').read_text(encoding='utf-8')
text = text.replace('₹', 'Rs. ').replace('–', '-').replace('—', '-').replace('×', 'x')
text = re.sub(r'\*\*|^#+\s*', '', text, flags=re.MULTILINE)
lines = []
for paragraph in text.splitlines():
    lines.extend(textwrap.wrap(paragraph, width=100, break_long_words=False) or [''])
pages = [lines[i:i+55] for i in range(0, len(lines), 55)]
objects = []
objects.append(b'<< /Type /Catalog /Pages 2 0 R >>')
kids = ' '.join(f'{4+2*i} 0 R' for i in range(len(pages)))
objects.append(f'<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>'.encode())
objects.append(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
for i, page in enumerate(pages):
    objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R >> >> /Contents {5+2*i} 0 R >>'.encode())
    commands = ['BT /F1 9 Tf 45 750 Td 12 TL']
    for line in page:
        safe = line.encode('latin-1', 'replace').decode('latin-1').replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
        commands.append(f'({safe}) Tj T*')
    commands.append('ET')
    stream = '\n'.join(commands).encode('latin-1')
    objects.append(f'<< /Length {len(stream)} >>\nstream\n'.encode()+stream+b'\nendstream')
pdf = bytearray(b'%PDF-1.4\n'); offsets = [0]
for i, obj in enumerate(objects, 1):
    offsets.append(len(pdf)); pdf.extend(f'{i} 0 obj\n'.encode()+obj+b'\nendobj\n')
xref = len(pdf); pdf.extend(f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode())
for offset in offsets[1:]: pdf.extend(f'{offset:010d} 00000 n \n'.encode())
pdf.extend(f'trailer << /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
(root/'MEMO.pdf').write_bytes(pdf)
print(f'Wrote MEMO.pdf ({len(pages)} pages)')
