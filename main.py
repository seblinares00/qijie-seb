from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import feedparser
from load_config import load_config
import json

config = load_config("config.ini")

llm = ChatOllama(
    model=config["llm_model"],
    temperature=0.9,
)

feed = feedparser.parse(r"https://www.ukri.org/opportunity/feed/")

with open("ukri.json", "w") as file:
    json.dump(feed, file, indent=4)

feed = feedparser.parse(r"http://www.govwire.co.uk/rss/innovate-uk")

with open("innovate.json", "w") as file:
    json.dump(feed, file, indent=4)

