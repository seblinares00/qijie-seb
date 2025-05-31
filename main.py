import langchain
import feedparser

feed = feedparser.parse(r"https://chemrxiv.org/engage/rss/chemrxiv")

print(feed)