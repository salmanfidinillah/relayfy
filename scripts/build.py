"""Produce deterministic static assets and check Python + JavaScript syntax."""
import compileall, hashlib, json, shutil, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
if not compileall.compile_dir(root/'service',quiet=1):sys.exit(1)
subprocess.run(['node','--check',str(root/'web/app.js')],check=True)
out=root/'dist';out.mkdir(exist_ok=True)
manifest={}
for src in sorted((root/'web').rglob('*')):
    if not src.is_file():continue
    filename=src.relative_to(root/'web');dest=out/filename;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    manifest[str(filename)]=hashlib.sha256(dest.read_bytes()).hexdigest()
(out/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Production assets built: '+str(out))
