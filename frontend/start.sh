#!/bin/bash

echo "Installing frontend dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Please check your network connection and try again."
    exit 1
fi

echo "Starting development server..."
npm run dev