#!/bin/bash
set -e

echo "Installing dependencies in react-frontend..."
cd react-frontend
npm install --legacy-peer-deps

echo "Building React app..."
CI=false npm run build

echo "Build complete!"
