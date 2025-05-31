# etl/extract.py

import requests

def get_top_story_ids(limit=10):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    return response.json()[:limit]

def get_story_details(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    response = requests.get(url)
    return response.json()

def extract_top_stories(limit=10):
    story_ids = get_top_story_ids(limit)
    stories = [get_story_details(sid) for sid in story_ids]
    return [
        {
            "title": story.get("title"),
            "url": story.get("url"),
            "by": story.get("by"),
            "time": story.get("time"),
            "id": story.get("id")
        }
        for story in stories if story
    ]

if __name__ == "__main__":
    from pprint import pprint
    pprint(extract_top_stories(5))