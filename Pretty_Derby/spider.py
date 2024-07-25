#spider
#采用aiohttp进行构建

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import re
from multiprocessing import pool


def save_to_json(data,file_path):
    with open(file_path,"w",encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=4)
    
async def fetch(url,session):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
            
    except aiohttp.ClientError as e:
        print(f"Request failed for {url}:{e}")
        return None
    

async def fetch_character_data(url,file_path,session):
        html=await fetch(url,session)
        if html:
            soup=BeautifulSoup(html,'html.parser')
        character_links=soup.find_all("a",href=re.compile(r"/umamusume/.+"),title=True)
        processed_characters=set()

        for link in character_links:
            character_name=link["title"]
            character_url="https://wiki.biligame.com"+link["href"]

            if character_url not in processed_characters:
                processed_characters.add(character_url)

                character_response=await fetch(character_url,session)
                if character_response:
                    character_soup=BeautifulSoup(character_response,"html.parser")

                    if character_soup:
                        Img_tag=character_soup.find("img",alt=re.compile(r"Jsf.+"))
                        if Img_tag:
                            image_url=Img_tag["src"]

                            gif_tag=character_soup.find("a",class_="image")
                            if gif_tag:
                                gif_url=gif_tag["href"]

                                character_data={
                                    "cuisine_name":character_name,
                                    "cuisine_image":image_url,
                                    "cuisine_gif":gif_url
                                }

                

        save_to_json(character_data,file_path)




async def fetch_skills_data(url,file_path,session):
    html=await fetch(url,session)
    if html:
        soup=BeautifulSoup(html,"html.parser")
    skill_table_soup=soup.find("table",id="CardSelectTr",class_="CardSelect wikitable sortable")
    skills=[]

    if skill_table_soup:
        rows=skill_table_soup.find_all('tr',class_="divsort")
        for row in rows:
            skills_title_title=row.find('a')['title']
            rarity=row['data-param1']
            description_tag=row.find('td',class_="visible-md visible-sm visible-lg",style="text-align: left;")
            description=description_tag.get_text(strip=True) if description_tag else "No description"
            skill_requirements=row['data-param4']

            skills.append({
                "name":skills_title_title,
                "description":description,
                "rarity":rarity,
                "Requirement":skill_requirements
            })

        save_to_json(skills,file_path)

    





async def fetch_competition(url):
    None

async def fetch_assistance_card(url):
    None







if __name__=="__main__":
    None
    with aiohttp.ClientSession() as session:
        fetch_skills_data()
        fetch_character_data()

