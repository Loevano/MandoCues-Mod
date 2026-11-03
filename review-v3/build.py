"""Build the small accepted changes on the preserved v2 layout."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'prototype/dist/index.html'
before=hashlib.sha256(BASE.read_bytes()).hexdigest()
source=BASE.read_text(encoding='utf-8')
source=source.replace('</style>','\n'+(ROOT/'minimal.css').read_text()+'\n</style>',1)
metadata=json.loads((ROOT/'version.json').read_text())
questions=json.loads((ROOT/'questions.json').read_text())
preamble='const activeProposalMeta='+json.dumps(metadata,ensure_ascii=False).replace('</','<\\/')+';\nconst activeProposalQuestions='+json.dumps(questions,ensure_ascii=False).replace('</','<\\/')+';\n'
scripts='\n'.join((ROOT/name).read_text() for name in ['minimal.js','note-times.js','best-takes.js','presentation-tour.js'])
source=source.replace('</body>','<script>\n'+preamble+scripts+'\n</script>\n</body>',1)
(ROOT/'index.html').write_text(source,encoding='utf-8')
assert hashlib.sha256(BASE.read_bytes()).hexdigest()==before
print('Built previous layout with cue drag handles and confirmed Space transport.')
