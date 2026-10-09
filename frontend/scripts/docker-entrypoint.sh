#!/bin/sh
set -e
# Named volume for node_modules can lag behind package-lock after new deps (e.g. recharts)
need_ci=0
for pkg in @mui/material recharts; do
  if [ ! -f "node_modules/${pkg}/package.json" ]; then
    need_ci=1
    break
  fi
done
if [ "$need_ci" -eq 1 ]; then
  echo "Installing frontend dependencies (npm ci)..."
  npm ci
fi
exec npm run dev -- --host 0.0.0.0 --port 5173
