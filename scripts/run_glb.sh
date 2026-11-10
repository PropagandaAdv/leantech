#!/bin/bash
cd "$(dirname "$0")/.."
for a in "PX0000381771 100000" "PX0000381774 100000" "PX0000381735 350000" "PX0000381687 350000" "PX0000380493 350000" "PX0000381782 350000" "PX0000381686 700000"; do
  set -- $a; echo "== $1"; python3 -I scripts/08_export_glb.py $1 $2 2>&1 | grep -E "facce saldate|triangoli|export|\.glb|Error|Traceback"
done
echo GLB_DONE
