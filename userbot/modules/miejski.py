import asyncio
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from bs4 import BeautifulSoup
import requests

@register(outgoing=True, pattern="^.miejski (.*)")
async def miejski(e):
    query = str(e.pattern_match.group(1))
    plus_query = query.replace(" ", "+")
    response = requests.get("https://www.miejski.pl/slowo-" + plus_query)
    if response.status_code == 404:
        return await e.edit(f"`Failed to find word {query}.`")
    parsed = BeautifulSoup(response.text, "html.parser")
    title = parsed.body.find("h1").get_text()
    definition = parsed.article.find("p").get_text()
    example = parsed.article.find("blockquote").get_text()
    await e.edit(title + "\n" + definition + "\n" + example)
    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID, f"Miejski query `{query}` was executed successfully")

CMD_HELP.update({
    "miejski":
    ">`.miejski <text>`"
    "\nUsage: Search miejski.pl database."
})
