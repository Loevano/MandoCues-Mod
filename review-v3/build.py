"""Build the small accepted changes on the preserved v2 layout."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'prototype/dist/index.html'
before=hashlib.sha256(BASE.read_bytes()).hexdigest()
source=BASE.read_text(encoding='utf-8')
source=source.replace('</style>','\n'+(ROOT/'minimal.css').read_text()+'\n</style>',1)
source=source.replace('</body>','<script>\n'+(ROOT/'minimal.js').read_text()+'\n</script>\n</body>',1)
(ROOT/'index.html').write_text(source,encoding='utf-8')
assert hashlib.sha256(BASE.read_bytes()).hexdigest()==before
print('Built previous layout with cue drag handles and confirmed Space transport.')
