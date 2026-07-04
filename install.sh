#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

if [ -n "$1" ]; then
    PROJECT_ID="$1"
fi

if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
fi

# Check if the PROJECT_ID environment variable is set
if [ -z "$PROJECT_ID" ]; then
    echo "Error: PROJECT_ID environment variable is not set."
    echo "Please run 'export PROJECT_ID=your-project-id' before executing this script."
    exit 1
fi

echo "Using Project ID: ${PROJECT_ID}"

echo "1. Installing and upgrading required Python packages..."
pip install --quiet --upgrade google-cloud-vectorsearch fsspec gcsfs google-auth google-api-core

echo "2. Creating GCS bucket (Location: asia-northeast1)..."
gcloud storage buckets create gs://${PROJECT_ID}-vs2 --location=asia-northeast1

echo "3. Copying dataset to the created GCS bucket..."
gcloud storage cp gs://jk-amazon-products-index/compact-records/amazon-product-dataset-768-compact.jsonl gs://${PROJECT_ID}-vs2/data/

echo "4. Running the index builder script..."
nohup python3 index_builder.py &

echo "All tasks completed successfully!"