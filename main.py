#!/usr/bin/env python3
import asyncio
import sys
from downloader import TikTokDownloader

async def main():
    print("🎵 TikTok Video Downloader")
    print("=" * 30)
    
    # Get URL from user input
    url = input("Please enter the TikTok URL: ").strip()
    
    # Optional: Get output directory
    output_dir = input("Output directory (press Enter for './downloads'): ").strip()
    if not output_dir:
        output_dir = "./downloads"
    
    downloader = TikTokDownloader()
    
    try:
        await downloader.download(url, output_dir)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())