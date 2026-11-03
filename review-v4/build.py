"""Build v4 without modifying the preserved v3 presentation."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'review-v3/index.html'
before=hashlib.sha256(BASE.read_bytes()).hexdigest()
source=BASE.read_text()
source=source.replace('</style>',(ROOT/'workspace.css').read_text()+'\n</style>',1)
modules=['planning-model.js','workspace.js','take-ranges.js','score-workspace.js','review.js']
scripts='\n'.join((ROOT/name).read_text() for name in modules)
source=source.replace('</body>','<script>\n'+scripts+'\n</script>\n</body>',1)
(ROOT/'index.html').write_text(source)
assert hashlib.sha256(BASE.read_bytes()).hexdigest()==before
print('Built local v4; preserved v3 and Comp tool unchanged.')
