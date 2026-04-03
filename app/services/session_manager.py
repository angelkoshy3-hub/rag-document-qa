import os
import shutil
from app.core.config import settings

def reset_session():
    """
    Delete and recreate storage directories to reset the current session.
    Ensures data privacy and prevents leakage between users or sessions.
    """
    directories = [settings.UPLOAD_DIR, settings.VECTOR_DB_DIR]
    
    for directory in directories:
        try:
            # Using shutil.rmtree to delete the entire directory tree
            # ignore_errors=True helps avoid issues with locked files on some OS
            if os.path.exists(directory):
                shutil.rmtree(directory, ignore_errors=True)
            
            # Recreate the clean directory after deletion
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            # For simplicity, we print and continue, but we could raise HTTPException in the route
            print(f"Error resetting directory {directory}: {str(e)}")
            continue

    return True
