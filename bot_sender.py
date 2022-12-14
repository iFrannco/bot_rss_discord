from functions import new_entries_db, update_entry
import requests
import os
from dotenv import load_dotenv


load_dotenv()
discord_bot = os.environ.get("webhook_key")
new_entries = new_entries_db()

for new in new_entries:
    data = {f"content":f"[{new['title']}]({new['link']})"}
    headers = {"Content-Type": "application/json"}
    requests.post(discord_bot, json=data, headers=headers)

    update_entry(new["link"])
