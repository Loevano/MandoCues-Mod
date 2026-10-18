"""Package a checked excerpt, never rewrite the original score books."""
from pathlib import Path
import base64
import hashlib
import json
from score_overview import add_score_overview

ASSETS=Path(__file__).resolve().parent/'src/score-assets'

def load_production_score():
    mapping=json.loads((ASSETS/'arrival-mapping.json').read_text())
    result=dict(mapping)
    result['pageImages']=['data:image/png;base64,'+base64.b64encode((ASSETS/name).read_bytes()).decode() for name in mapping['images']]
    result['pdfData']=base64.b64encode((ASSETS/mapping['pdf']).read_bytes()).decode()
    original=ASSETS.parents[2]/'06_SCORES'/mapping['sourceFile']
    if original.exists():
        assert hashlib.sha256(original.read_bytes()).hexdigest()==mapping['sourceSha256'], 'Score book changed; review the excerpt and mapping before rebuilding.'
    assert [r['measure'] for r in mapping['regions']]==list(range(1,42))
    result['staffLabels']=json.loads((ASSETS/'staff-labels.json').read_text())
    add_score_overview(result)
    return result
