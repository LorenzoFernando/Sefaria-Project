#!/bin/bash
set -e

echo "Waiting for the test job to become ready"
echo "GitHub Run ID $GITHUB_RUN_ID"

kubectl get jobs -l test-name=pytest -o json

timeout ${WAIT_DURATION:-900} bash -c "while [[ $(kubectl get job -l ci-run=$GITHUB_RUN_ID,test-name=${TEST_NAME:-pytest} -o json | jq -r '.items[0].status.succeeded') != 1 ]]; do sleep 5; done"

echo "Job is complete"