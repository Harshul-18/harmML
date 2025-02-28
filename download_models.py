#!/usr/bin/env python3
"""
Script to download model files from an external source.
This allows you to keep large model files out of your Git repository.
"""

import os
import sys
import subprocess
import zipfile
from tqdm import tqdm

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# URL to your models zip file (replace with your actual URL)
# You can use services like Google Drive, Dropbox, or any file hosting service
MODELS_URL = "https://drive.google.com/file/d/1Yr0tAHaHKUdFFFbLC538CVrmjjEnbLzJ/view?usp=sharing"  # Replace with your actual URL
MODELS_ID = "1Yr0tAHaHKUdFFFbLC538CVrmjjEnbLzJ"  # The file ID extracted from the URL

def install_gdown():
    """
    Install gdown if not already installed
    """
    try:
        import gdown
        print("gdown is already installed.")
        return True
    except ImportError:
        print("gdown is not installed. Installing now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
            print("gdown installed successfully.")
            return True
        except Exception as e:
            print(f"Failed to install gdown: {e}")
            return False

def download_from_google_drive(file_id, destination):
    """
    Download a file from Google Drive using gdown
    """
    try:
        import gdown
        
        print(f"Downloading file from Google Drive (ID: {file_id})...")
        output = gdown.download(
            id=file_id,
            output=destination,
            quiet=False
        )
        
        if output:
            print(f"Download complete: {destination}")
            return True
        else:
            print("Download failed.")
            return False
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """
    Extract a zip file
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            print(f"Extracting {zip_path} to {extract_to}...")
            
            # Get total number of files for progress bar
            total_files = len(zip_ref.namelist())
            
            # Extract with progress bar
            for i, file in enumerate(zip_ref.namelist()):
                zip_ref.extract(file, extract_to)
                # Update progress every 10 files to avoid too many updates
                if i % 10 == 0 or i == total_files - 1:
                    progress = (i + 1) / total_files * 100
                    print(f"Extraction progress: {progress:.1f}% ({i+1}/{total_files})")
                    
        print("Extraction complete!")
        return True
    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid ZIP file.")
        print("This often happens with Google Drive files. Please check:")
        print("1. The file on Google Drive is actually a ZIP file")
        print("2. The file is not too large (>2GB) for direct download")
        print("3. Try downloading the file manually and placing it in the models directory")
        
        # Provide manual download instructions
        print("\nManual download instructions:")
        print(f"1. Open this URL in your browser: {MODELS_URL}")
        print("2. Download the file by clicking the download button")
        print("3. Save the file as 'models.zip' in the same directory as this script")
        print("4. Run this script again to extract the models")
        
        return False
    except Exception as e:
        print(f"Error extracting zip file: {e}")
        return False

def main():
    """
    Main function to download and extract models
    """
    # Check if models already exist
    model_files = [
        "business_model.pkl", "cat_model.pkl", "coding_model.pkl",
        "competitive_exams_model.pkl", "design_model.pkl", "edu_model.pkl",
        "educated_model.pkl", "finance_and_accounting_model.pkl",
        "health_and_fitness_model.pkl", "it_and_software_model.pkl",
        "lifestyle_model.pkl", "marketing_model.pkl", "model.pkl",
        "music_model.pkl", "office_productivity_model.pkl",
        "personal_development_model.pkl", "photography_and_video_model.pkl",
        "teaching_and_academics_model.pkl", "vectorizer.pkl"
    ]
    
    # Check if all model files exist
    all_models_exist = all(os.path.exists(os.path.join('models', model)) for model in model_files)
    
    if all_models_exist:
        print("All model files already exist. Skipping download.")
        return
    
    # Check if models.zip already exists
    zip_path = "models.zip"
    if os.path.exists(zip_path):
        print(f"Found existing {zip_path}. Skipping download.")
    else:
        # Install gdown if needed
        if not install_gdown():
            print("Failed to install gdown. Please install it manually with: pip install gdown")
            sys.exit(1)
        
        # Download zip file
        if not download_from_google_drive(MODELS_ID, zip_path):
            print("Failed to download models. Please check the URL and try again.")
            print("You can also try downloading the file manually and placing it in this directory.")
            sys.exit(1)
    
    # Extract zip file
    if not extract_zip(zip_path, '.'):
        print("Failed to extract models. Please check the zip file and try again.")
        sys.exit(1)
    
    # Clean up zip file
    try:
        os.remove(zip_path)
        print(f"Removed temporary file: {zip_path}")
    except Exception as e:
        print(f"Warning: Could not remove temporary file {zip_path}: {e}")
    
    print("Model download and setup complete!")

if __name__ == "__main__":
    main()
