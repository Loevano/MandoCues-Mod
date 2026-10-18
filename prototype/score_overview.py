"""Cue index for the supplied score export, not a general PDF recognizer.
Printed bar numbers locate approximate hit areas. Compressed rests are not
expanded into invented measure positions. Arrival keeps its reviewed mapping.
"""
from pathlib import Path
import base64,json
ASSETS=Path(__file__).resolve().parent/'src/score-assets'

def add_score_overview(production):
    book=json.loads((ASSETS/'score-catalog.json').read_text())['books'][0]
    pages=json.loads((ASSETS/'overview/printed-numbers.json').read_text())
    documents=[]
    images={}
    for cue in book['cuePages']:
        if cue['cue']=='1M02':continue
        book_pages=list(range(cue['startPage'],cue['endPage']+1))
        regions=[]
        for index,p in enumerate(book_pages):
            numbers=pages[p-1]['numbers']
            rows=[]
            for n in sorted(numbers,key=lambda a:(a['y'],a['x'])):
                if not (10.5<n['size']<11.2 and n['x']>.18):continue
                row=next((r for r in rows if abs(r[0]['y']-n['y'])<.003),None)
                if row is None:rows.append([n])
                else:row.append(n)
            for row in rows:
                row.sort(key=lambda n:n['x'])
                assert all(a['n']<b['n'] for a,b in zip(row,row[1:])),(cue,p)
                labels=[n for n in numbers if n['n']==1 and n['x']<.18 and n['y']<row[0]['y'] and 11.5<n['size']<12.2]
                top=max(n['y'] for n in labels)-.012 if labels else max(.07,row[0]['y']-.34)
                bottom=min(.99,row[0]['y']+max(n['h'] for n in row)+.004)
                centers=[n['x']+n['w']/2 for n in row]
                edges=[max(.16,centers[0]-(centers[1]-centers[0])/2) if len(row)>1 else .17]
                edges += [(a+b)/2 for a,b in zip(centers,centers[1:])]+[.94]
                for i,n in enumerate(row):
                    regions.append(dict(measure=n['n'],page=index+1,bookPage=p,x=round(edges[i],6),y=round(top,6),width=round(edges[i+1]-edges[i],6),height=round(bottom-top,6)))
            images[str(p)]='data:image/webp;base64,'+base64.b64encode((ASSETS/f'overview/book-{p}.webp').read_bytes()).decode()
        assert regions and len({r['measure'] for r in regions})==len(regions),cue
        documents.append(dict(id='afterparty-full-v3-'+production['sourceSha256'][:12]+'-'+cue['cue'],cue=cue['cue'],name='After Party · '+cue['cue']+' · Full score v3',pages=len(book_pages),bookPages=book_pages,measureRange=[regions[0]['measure'],regions[-1]['measure']],regions=regions,mapping='Benaderde vakken vanuit gedrukte maatnummers; meermaatsrusten niet opgesplitst.'))
    production['documents']=documents
    production['bookImages']=images
