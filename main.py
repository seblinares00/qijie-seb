import feedparser
import json

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime, timezone

from load_config import load_config

config = load_config("config.ini")

llm = ChatOllama(
    model=config["llm_model"],
    temperature=0.9,
)

# setting the retrieved time to the 1/1/1900 if it doesn't exist
if config["rss_last_retrieved"] == "":
    config["rss_last_retrieved"] = datetime(1900,1,1,0,0, tzinfo=timezone.utc)

# setting the system message
llm_system_message = """You are a helpful classifer of topics. 
            Only respond with Yes or No as classification. 
            Do not elborate. Do not respond with words other than yes or no."""

topic_list = {}
for topic in config["topics"]:
    topic_list[topic] = []

for rss in config["rss"]:
    feed = feedparser.parse(rss)
    for entry in feed["entries"]:
        # checking when the rss was published, if it was before when we retrieved it
        if datetime(*entry["published_parsed"][:5], tzinfo=timezone.utc) < config["rss_last_retrieved"]:
            break
        else:
            for topic in config["topics"]:
                query = [
                    SystemMessage(llm_system_message),
                    HumanMessage(f'Is "{entry["title"]}" related to {topic}?')
                ]
                response = llm(query)
                if "yes" in response.content.lower():
                    topic_list[topic].append({"title": entry["title"],
                                            "summary": entry["summary"],
                                            "link": entry["link"]})

config["rss_last_retrieved"] = datetime.now(tz=timezone.utc)
with open("output.json", "w") as file:
    json.dump(topic_list, file, indent=4)