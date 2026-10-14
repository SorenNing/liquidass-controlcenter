#!/usr/bin/env python3
"""Read-only audit for a macOS-built roothide DEB. Refuses unsafe loader shapes."""
import plistlib, subprocess, sys, tempfile, pathlib, re
p=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else tempfile.mkdtemp())
out.mkdir(parents=True,exist_ok=True)
def run(*a): return subprocess.check_output(a,text=True,stderr=subprocess.STDOUT)
print(run('dpkg-deb','-f',str(p),'Package','Version','Architecture','Depends'))
subprocess.check_call(['dpkg-deb','-x',str(p),str(out)])
for f in sorted(out.rglob('*.dylib')):
 h=run('otool','-l',str(f)); deps=run('otool','-L',str(f)); print('\n',f,'\n',deps)
 if 'LC_DYLD_CHAINED_FIXUPS' not in h: raise SystemExit('missing chained fixups: '+str(f))
 if 'LC_CODE_SIGNATURE' not in h: raise SystemExit('missing signature: '+str(f))
 if 'libSystemStub' in deps or 'TestCC' in deps: raise SystemExit('experimental dependency: '+str(f))
 if 'undefined dynamic_lookup' in deps: raise SystemExit('dynamic lookup marker: '+str(f))
for f in out.rglob('*.plist'):
 try:
  b=f.read_bytes(); fmt=plistlib.FMT_BINARY if b[:8]==b'bplist00' else plistlib.FMT_XML; print('plist',f,plistlib.loads(b,fmt=fmt))
 except Exception as e: raise SystemExit('bad plist '+str(f)+': '+str(e))
print('AUDIT PASS: metadata, plist, chained fixups and dependency gate')
