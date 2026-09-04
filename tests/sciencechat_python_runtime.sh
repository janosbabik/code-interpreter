#!/usr/bin/env bash

set -euo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
requirements="$root/python-packages-extra.txt"

for requirement in \
  'sans-fitter==0.3.0' \
  'bumps==1.0.3' \
  'sasmodels==1.1.0' \
  'sasdata==0.12.2' \
  'scipp==26.8.0' \
  'scippnexus==26.1.1' \
  'scippneutron==26.9.0' \
  'essreduce==26.8.0' \
  'esssans==26.6.0' \
  'essdiffraction==26.8.1' \
  'essimaging==26.9.0' \
  'essnmx==26.6.0' \
  'essreflectometry==26.6.0' \
  'essspectroscopy==26.7.0' \
  'orsopy==1.2.3' \
  'refnx==0.1.67' \
  'diffpy.srfit==3.3.1' \
  'euphonic==2.1.0'; do
  grep -Fx "$requirement" "$requirements" >/dev/null
done

while IFS= read -r requirement; do
  [[ "$requirement" =~ ^[[:space:]]*(#|$) ]] && continue
  if [[ "$requirement" != *"=="* ]]; then
    echo "Unpinned ScienceChat requirement: $requirement" >&2
    exit 1
  fi
done < "$requirements"

grep -F 'PYTHON_EXTRA_PACKAGES_FILE' "$root/docker/package-init.sh" >/dev/null
grep -F 'precompile-sasmodels.py' "$root/docker/Dockerfile.package-init" >/dev/null
grep -F 'precompile-sasmodels.py' "$root/api/Dockerfile" >/dev/null
grep -F 'precompile-sasmodels.py' "$root/docker/Dockerfile.worker-sandbox" >/dev/null
grep -F 'ARG PYTHON_VERSION=3.14.4' "$root/api/Dockerfile" >/dev/null
grep -F 'ARG PYTHON_VERSION=3.14.4' "$root/docker/Dockerfile.worker-sandbox" >/dev/null
grep -F 'CODEAPI_PYTHON_VERSION' "$root/service/src/config.ts" >/dev/null
grep -F 'CODEAPI_PYTHON_VERSION' "$root/helm/codeapi/templates/api-deployment.yaml" >/dev/null
grep -F 'CODEAPI_PYTHON_VERSION' "$root/helm/codeapi/templates/worker-sandbox-deployment.yaml" >/dev/null
grep -F 'pythonRuntimeVersion: "3.12.12"' "$root/helm/codeapi/values.yaml" >/dev/null

pycache=$(mktemp -d)
trap 'rm -rf "$pycache"' EXIT
PYTHONPYCACHEPREFIX="$pycache" python3 -m py_compile "$root/docker/precompile-sasmodels.py"

echo "ScienceChat Python runtime configuration checks passed."
