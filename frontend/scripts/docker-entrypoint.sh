#!/bin/sh
set -e
# Named volume for node_modules can lag behind package.json after Phase 6+ deps
if [ ! -f node_modules/@mui/material/package.json ]; then
  echo "Installing frontend dependencies (npm ci)..."
  npm ci
fi
exec npm run dev -- --host 0.0.0.0 --port 5173
