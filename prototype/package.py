"""Archive the generated offline handoff, with no source files or local data."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parent
dist=root/'dist'
archive=root.parent/'MandoCues-prototypes-van-Floris.zip'
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
    for f in sorted(dist.iterdir()):
        if f.is_file():z.write(f,'Prototypes-van-Floris/'+f.name)
print(f'Packaged {len(list(dist.iterdir()))} files: {archive.name} ({archive.stat().st_size:,} bytes)')
