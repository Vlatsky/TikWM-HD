# downloader.py
import os
import aiohttp
import aiofiles
from api import TikWMAPI
from utils import (
    check_file_exists, 
    display_progress, 
    format_bytes, 
    generate_filename, 
    prompt_overwrite, 
    validate_tiktok_url
)

class TikTokDownloader:
    def __init__(self):
        self.api = TikWMAPI()

    async def download_file(self, download_url: str, filename: str, output_dir: str) -> None:
        full_path = os.path.join(output_dir, filename)
        print(f"\n📥 Downloading to: {full_path}")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                download_url,
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
            ) as response:
                if response.status != 200:
                    raise Exception(f"Download failed! Status: {response.status}")
                
                content_length = response.headers.get("content-length")
                total_size = int(content_length) if content_length else 0
                downloaded_size = 0

                async with aiofiles.open(full_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)
                        downloaded_size += len(chunk)
                        display_progress(downloaded_size, total_size)
        
        print(f"\n✅ Download completed: {filename}")

    def display_video_info(self, result: dict) -> None:
        detail = result["detail"]
        print(f"\n📹 Title: {detail['title']}")
        print(f"👤 Author: {detail['author']['nickname']} (@{detail['author']['unique_id']})")
        print(f"⏱️  Duration: {detail['duration']}s")
        print(f"📊 Size: {format_bytes(detail['size'])}")

    async def download(self, url: str, output_dir: str = "./downloads") -> None:
        if not validate_tiktok_url(url):
            raise Exception("Please provide a valid TikTok URL")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        print("🔄 Submitting download request...")
        task_id = await self.api.submit_task(url)

        print("⏳ Processing video...")
        result = await self.api.get_task_result(task_id)

        filename = generate_filename(result["detail"]["author"]["unique_id"], result["detail"]["id"])
        full_path = os.path.join(output_dir, filename)

        # Check if file exists
        if check_file_exists(full_path):
            should_overwrite = await prompt_overwrite(filename)
            if not should_overwrite:
                print("✅ Download cancelled.")
                return
            print("📝 Proceeding with overwrite...")

        self.display_video_info(result)
        await self.download_file(result["detail"]["download_url"], filename, output_dir)