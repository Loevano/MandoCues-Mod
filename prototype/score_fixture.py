"""Original schematic score fixture, rendered from the same geometry to SVG and PDF."""
import base64


def make_fixture():
    pages, streams = [], []
    for page in range(2):
        svg = ['<svg viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Schematic demo score for string quartet">', '<rect width="900" height="560" fill="#fffdf7"/>']
        pdf = ['0.15 0.15 0.15 rg', '0.15 0.15 0.15 RG']

        def line(x1, y1, x2, y2, width=.7):
            svg.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="#36352f" stroke-width="{width}"/>')
            pdf.append(f'{width} w {x1} {560-y1} m {x2} {560-y2} l S')

        def text(x, y, value, size=12, italic=False):
            svg.append(f'<text x="{x}" y="{y}" fill="#34332e" font-family="Georgia,serif" font-size="{size}"'+(' font-style="italic"' if italic else '')+f'>{value}</text>')
            safe = value.replace('(', '\\(').replace(')', '\\)')
            pdf.append(f'BT /F1 {size} Tf {x} {560-y} Td ({safe}) Tj ET')

        text(110, 34, '1M02 - Arrival', 22)
        text(110, 55, 'String quartet - schematic demo score', 11)
        text(745, 34, f'Page {page+1} / 2', 11)
        for system in range(2):
            top = 100 + system*225
            for staff, name in enumerate(['Violin I', 'Violin II', 'Viola', 'Cello']):
                y = top+staff*37
                text(25, y+14, name, 11)
                for ln in range(5):
                    line(110, y+ln*4, 850, y+ln*4, .5)
                for bar in range(5):
                    line(110+bar*185, y, 110+bar*185, y+16)
                if staff == 0:
                    text(110, y-12, 'Andante' if system == 0 else 'dolce', 11, True)
                for bar in range(4):
                    number = 17+page*8+system*4+bar
                    if staff == 0:
                        text(120+bar*185, y-27, str(number), 12)
                    for n in range(4):
                        x = 133+bar*185+n*41
                        ny = y+4+((bar*2+n+staff+page)%7)*2
                        svg.append(f'<ellipse cx="{x}" cy="{ny}" rx="4.6" ry="3.1" transform="rotate(-15 {x} {ny})" fill="#282721"/>')
                        # Four cubic segments approximate the same notehead in the PDF.
                        py=560-ny
                        pdf.append(f'{x-4.6} {py} m {x-4.6} {py+4.2} {x+4.6} {py+4.2} {x+4.6} {py} c {x+4.6} {py-4.2} {x-4.6} {py-4.2} {x-4.6} {py} c f')
                        line(x+4, ny, x+4, ny-22, 1)
                if staff == 3:
                    text(121, y+35, 'p', 15, True)
            line(106, top, 106, top+127, 1.8)
        text(110, 535, 'Original demo excerpt; not a production score.', 10)
        svg.append('</svg>')
        pages.append(''.join(svg))
        streams.append('\n'.join(pdf).encode('ascii'))

    objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [4 0 R 6 0 R] /Count 2 >>', b'<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >>']
    for idx, stream in enumerate(streams):
        objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 900 560] /Resources << /Font << /F1 3 0 R >> >> /Contents {5+idx*2} 0 R >>'.encode())
        objects.append(b'<< /Length '+str(len(stream)).encode()+b' >>\nstream\n'+stream+b'\nendstream')
    data = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    for n, obj in enumerate(objects, 1):
        offsets.append(len(data));data.extend(f'{n} 0 obj\n'.encode()+obj+b'\nendobj\n')
    xref=len(data)
    data.extend(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]:data.extend(f'{offset:010d} 00000 n \n'.encode())
    data.extend(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    return {'pages':pages,'pdf':base64.b64encode(data).decode()}
