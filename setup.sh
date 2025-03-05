#!/bin/bash

# Create a Python 3.11 environment for Illuminai
echo "Setting up Python 3.11 environment for Illuminai..."

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "Creating conda environment with Python 3.11..."
    conda create -y -n illuminai-py311 python=3.11
    conda activate illuminai-py311
    
    # Install dependencies
    echo "Installing Python dependencies..."
    pip install -r src/backend/requirements.txt
    
    echo "Environment setup complete. Activate it with:"
    echo "conda activate illuminai-py311"
else
    # If conda is not available, try to use virtualenv
    echo "Conda not found. Trying with virtualenv..."
    
    # Check if Python 3.11 is available
    if command -v python3.11 &> /dev/null; then
        echo "Creating virtual environment with Python 3.11..."
        python3.11 -m venv illuminai-venv
        source illuminai-venv/bin/activate
        
        # Install dependencies
        echo "Installing Python dependencies..."
        pip install -r src/backend/requirements.txt
        
        echo "Environment setup complete. Activate it with:"
        echo "source illuminai-venv/bin/activate"
    else
        echo "Python 3.11 not found. Please install Python 3.11 and try again."
        echo "You can download it from https://www.python.org/downloads/"
        exit 1
    fi
fi

# Set up database
echo "Setting up database..."
cd src/backend/database/migrations
alembic upgrade head
cd ../../../..

echo "Setup complete! To start the application:"
echo "1. Backend: cd src/backend && uvicorn main:app --reload"
echo "2. Frontend: cd src/frontend && npm install && npm run dev"