"""
Environment configuration management
Centralized dotenv handling - loads ALL environment variables dynamically
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in project root
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Export all environment variables dynamically
env_vars = dict(os.environ)

# Make all env vars available as module attributes
globals().update(env_vars)

# Also make them available as a dictionary for easy access
ENV = env_vars