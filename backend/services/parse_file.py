import os
import json
from pathlib import Path

from docling import DocumentConverter

paths = Path("uploads")
   
file_paths = [str(item.resolve()) for item in paths.iterdir() if item.is_file()]

converter = DocumentConverter(allowed =  [".pdf",".json",".txt"])

# for file_path in file_paths:


