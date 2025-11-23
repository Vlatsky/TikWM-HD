# api.py
import json
import aiohttp
import asyncio
from typing import Dict, Any

class TikWMAPI:
    def __init__(self):
        self.base_url = "https://www.tikwm.com/api/video"
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

    async def submit_task(self, url: str) -> str:
        form_data = aiohttp.FormData()
        form_data.add_field("url", url)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/task/submit",
                data=form_data,
                headers={"User-Agent": self.user_agent}
            ) as response:
                if response.status != 200:
                    raise Exception(f"HTTP error! Status: {response.status}")
                
                data = await response.json()
                if data.get("code") != 0:
                    raise Exception(f"API error: {data.get('msg')}")
                
                return data["data"]["task_id"]

    async def get_task_result(self, task_id: str, max_retries: int = 10) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            for i in range(max_retries):
                async with session.get(
                    f"{self.base_url}/task/result?task_id={task_id}",
                    headers={"User-Agent": self.user_agent}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"HTTP error! Status: {response.status}")
                    
                    data = await response.json()
                    
                    # with open('video_data.json', 'w', encoding='utf-8') as f:
                    #     json.dump(data, f, ensure_ascii=False, indent=4)
                    
                    if data.get("code") != 0:
                        raise Exception(f"API error: {data.get('msg')}")
                    
                    # Status 2 means processing complete
                    if (data["data"].get("status") == 2 and 
                        data["data"]["detail"].get("download_url")):
                        return data["data"]
                
                # Wait before retrying
                await asyncio.sleep(2)
                if i < max_retries - 1:
                    print(".", end="", flush=True)
            
            raise Exception("Video processing timed out. Please try again later.")