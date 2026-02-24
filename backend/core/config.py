import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Vector Store
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    QDRANT_API_KEY:str = os.getenv("QDRANT_API_KEY")

    # Model Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")

    #file storage settings
    SUPABASE_URL:str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY:str = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET:str = os.getenv("SUPABASE_BUCKET")
   
    
  