import random

def doc_to_text(doc):
    templates = ["Consider the news headline - does it concern {}?",
        "Examine the news headline and decide if it includes {}.",
        "Let me know if the news headline talks about {}.",
        "Please determine if the news headline addresses {}.",
        "In the context of the news headline, is {} discussed?",
        "Interpret the news headline to see if it mentions {}.",
        "Is the news headline related to {}?",
        "Analyze the news headline for any mention of {}.",
        "Assess if the news headline touches on {}.",
        "Does the news headline talk about {}?",
        "Review the news headline and determine if it relates to {}.",]

    topic_map = {
        "PastPrice": "price in the past",
        "FuturePrice": "price in the future",
        "PastNews": "a general event (apart from prices) in the past",
        "FutureNews": "a general event (apart from prices) in the future",
        "Asset Comparison": "comparing gold with any other asset",
        "Price or Not": "price",
        "Direction Up": "price going up",
        "Direction Down": "price going down",
        "Direction Constant": "price staying constant",}

    query = doc["query"]
    query_topic = [v for k,v in topic_map.items() if k in query][0]

    return templates[random.randrange(len(templates))].format(query_topic)