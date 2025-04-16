from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define static and stories directories
STATIC_DIR = os.path.join(BASE_DIR, "static")
CUENTOS_DIR = os.path.join(STATIC_DIR, "CuentosGenerados")
IMAGENES_DIR = os.path.join(STATIC_DIR, "ImagenesGeneradas")

# Create directories if they don't exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(CUENTOS_DIR, exist_ok=True)
os.makedirs(IMAGENES_DIR, exist_ok=True)

# Debug logging
print(f"BASE_DIR: {BASE_DIR}")
print(f"STATIC_DIR: {STATIC_DIR}")
print(f"CUENTOS_DIR: {CUENTOS_DIR}")
print(f"Static directory: {STATIC_DIR}")
print(f"Cuentos directory: {CUENTOS_DIR}")
print(f"Imagenes directory: {IMAGENES_DIR}")

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')