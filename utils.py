# utils.py
import os
import re
import math
from typing import Union

def check_file_exists(filepath: str) -> bool:
    return os.path.exists(filepath)

async def prompt_overwrite(filename: str) -> bool:
    print(f"\n⚠️  File {filename} already exists.")
    print("Overwrite?")
    
    while True:
        try:
            choice = input("Choice (y/N): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no', '']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no: ")
        except EOFError:
            return False

def format_bytes(bytes: int) -> str:
    if bytes == 0:
        return "0 B"
    k = 1024
    sizes = ["B", "KB", "MB", "GB"]
    i = math.floor(math.log(bytes) / math.log(k))
    return f"{round(bytes / (k ** i), 1)} {sizes[i]}"

def validate_tiktok_url(url: str) -> bool:
    tiktok_url_regex = r"^https?:\/\/(www\.)?(tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)"
    return bool(re.match(tiktok_url_regex, url))

def generate_filename(author: str, video_id: str) -> str:
    return f"{author}_{video_id}.mp4"

def display_progress(downloaded_size: int, total_size: int) -> None:
    if total_size > 0:
        progress = round((downloaded_size / total_size) * 100, 1)
        downloaded = format_bytes(downloaded_size)
        total = format_bytes(total_size)
        print(f"\r📊 Progress: {progress}% ({downloaded}/{total})", end="", flush=True)