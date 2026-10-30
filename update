#!/bin/bash
branch="develop"
if test $# -ne 1; then
    echo "Defaulting to develop branch..."
else
    branch=${1}
fi

echo "Fetching..."
git fetch --all --prune &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error fetching the latest."
    exit 1
fi

echo "Checking out ${branch}..."
git checkout ${branch} &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error checking out ${branch}. Does it exist?"
    exit 1
fi

echo "Getting latest code..."
git pull &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error pulling the latest code."
    exit 1
fi
