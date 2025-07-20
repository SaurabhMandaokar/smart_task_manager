#!/bin/bash

# Step 1: Navigate to project
cd ~/documents/dev/smart_task_manager || {
  echo "❌ Directory not found!"; exit 1;
}

# Step 2: Activate virtual environment
if [ -d "venv" ]; then
  source venv/bin/activate
else
  echo "❌ Virtual environment not found!"
  exit 1
fi

# Step 3: Open browser (macOS)
open http://127.0.0.1:5050

# Step 4: Run Flask backend
echo "🚀 Launching Flask server at http://127.0.0.1:5050"
python3 backend/app.py
