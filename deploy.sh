#!/bin/bash

# Deployment preparation script for SRGAN API

echo "1. Checking Python version..."
python --version

echo "2. Installing Vercel CLI if not present..."
if ! command -v vercel &> /dev/null; then
    npm install -g vercel
fi

echo "3. Building and deploying to Vercel..."
vercel deploy --prod

echo "4. Deployment complete! Testing endpoints..."
DEPLOY_URL=$(vercel --prod)
curl "${DEPLOY_URL}/api/status"

echo "Deployment URL: ${DEPLOY_URL}"