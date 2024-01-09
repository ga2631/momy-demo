import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

FACESHAPE_TOKEN=os.getenv('FACESHAPE_TOKEN')
HUGGINGFACE_API_TOKEN=os.getenv('HUGGINGFACE_API_TOKEN')