import asyncio
import aiohttp
import re
import json
from bs4 import BeautifulSoup
from Pretty_Derby import configs,spider

async def main():
    async with aiohttp.ClientSession() as session:
        character_url=configs.character_url
        skills_url=configs.skill_url
        character_file_path=r"D:\desktop\Pretty_Derby\character.json"
        skills_file_path=r"D:\desktop\Pretty_Derby\skills.json"

        await spider.fetch_skills_data(skills_url,skills_file_path,session)
        await spider.fetch_character_data(character_url,character_file_path,session)


asyncio.run(main())