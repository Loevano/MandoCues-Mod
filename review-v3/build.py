"""Build the isolated v3 review, leaving the v2 demo and hosting copy unchanged."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'prototype/dist/index.html'
source=BASE.read_text(encoding='utf-8')
before=hashlib.sha256(BASE.read_bytes()).hexdigest()
css=(ROOT/'review.css').read_text(encoding='utf-8')
js='\n'.join((ROOT/name).read_text(encoding='utf-8') for name in ('review.js','sections.js','note-ranges.js','planner.js','cue-order.js','clocks.js','reference-score.js','review-tour.js') if (ROOT/name).is_file())
assert '</style>' in source and '</body>' in source
source=source.replace('</style>', '\n'+css+'\n</style>',1)
source=source.replace('</body>', '<script>\n'+js+'\n</script>\n</body>',1)
(ROOT/'index.html').write_text(source,encoding='utf-8')
assert hashlib.sha256(BASE.read_bytes()).hexdigest()==before
print('Built isolated v3 review: '+str(ROOT/'index.html'))
