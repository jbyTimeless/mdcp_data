import uvicorn
import os
import sys

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    uvicorn.run("services.dataset.main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=[".."])
