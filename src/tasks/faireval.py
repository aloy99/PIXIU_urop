import random

FPB_PROMPTS = {
    "template":
    [
        "Evaluate the sentiment conveyed in this excerpt from a financial news report. Classify your response as positive, negative, or neutral.",
        "Determine the sentiment expressed in this financial journalism snippet. Categorize your assessment as neutral, positive, or negative.",
        "Interpret the sentiment present in this extract from a piece of business news. Present your conclusion as negative, neutral, or positive.",
        "Assess the sentiment in this market news excerpt. Indicate your judgment as positive, neutral, or negative.",
        "Examine the sentiment of this financial news snippet. State your analysis as neutral, negative, or positive."
    ]
}

FIQASA_PROMPTS = [
    "template":
    [
        "Analyze the sentiment of this financial {category_0}. Classify your response as Positive, Negative, or Neutral?",
        "Evaluate the sentiment conveyed in the given financial {category_0}. Categorize your assessment as Positive, Negative, or Neutral.",
        "Determine the sentiment expressed in this financial {category_0}. Present your conclusion as Positive, Negative, or Neutral.",
        "Assess the sentiment of the presented financial {category_0}. Indicate your judgment as Positive, Negative, or Neutral.",
        "Interpret the sentiment of the following financial {category_0}. State your analysis as Positive, Negative, or Neutral."
    ],
    0: {
        "post": [
            "post",
        ]
        "headline": [
            "headline"
        ]
    }
]

NER_PROMPTS = {
    "template":
    [
        "For text snippets taken from financial agreements in United States Securities and Exchange Commission documents, detect entities categorized as individuals ('PER'), companies ('ORG'), or places ('LOC'). Present results as: 'entity name, entity type'.",
        "Locate and classify named entities within excerpts from financial agreements found in SEC filings. Identify persons ('PER'), organizations ('ORG'), and locations ('LOC'). Format your response as: 'entity name, entity type'.",
        "Analyze passages from financial contracts submitted to the U.S. SEC. Pinpoint entities that are people ('PER'), institutions ('ORG'), or geographical areas ('LOC'). List findings as: 'entity name, entity type'.",
        "Extract and categorize named entities from financial agreement segments in Securities and Exchange Commission reports. Tag humans ('PER'), groups ('ORG'), and sites ('LOC'). Output should be: 'entity name, entity type'.",
        "Within financial contract excerpts from SEC-filed documents, recognize entities representing individuals ('PER'), corporations ('ORG'), or territories ('LOC'). Structure answers as: 'entity name, entity type'."
    ]
}

HEADLINE_PROMPTS = {
    "template":
    [
        "Is {category_0} a topic covered in the news headline? Respond with either Yes or No.",
        "Does the news title address {category_0}? Your answer should be limited to Yes or No.",
        "Can information about {category_0} be found in the news headline? Reply with Yes or No only.",
        "Evaluate if the news headline contains information about {category_0}. Provide a Yes or No response.",
        "Determine whether {category_0} is referenced in the news headline. Answer exclusively with Yes or No."
    ],
    0: {
        "Price or Not": [
            "price"
        ],
        "Direction Up": [
            "price going up"
        ],
        "Direction Constant": [
            "price staying constant"
        ],
        "Direction Down": [
            "price going down"
        ],
        "PastPrice": [
            "price in the past"
        ],
        "FuturePrice": [
            "price in the future"
        ],
        "PastNews": [
            "a general event (apart from prices) in the past"
        ],
        "FutureNews": [
            "a general event (apart from prices) in the future"
        ],
        "Asset Comparison": [
            "comparison of gold with any other asset"
        ]
    }
}

FINQA_PROMPTS = {
    "template":
    [
        "Using the provided context, respond to the presented financial inquiry.",
        "Address the given financial question, drawing from the provided background information.",
        "Based on the supplied context, offer an answer to the specified financial query.",
        "Referring to the contextual details provided, tackle the stated financial question.",
        "Utilize the given context to formulate a response to the posed financial inquiry."
    ]
}

CONVFINQA_PROMPTS = {
    "template":
    [
        "Based on the sequence of linked financial inquiries and the supplementary details given in the pretext, tables, and posttext from corporate fiscal reports, answer the concluding question. This may involve data extraction and numerical computations. Consider all prior questions and their responses when crafting your answer.",
        "Utilizing the chain of related financial questions and the contextual data from company monetary documents (including pretext, tables, and posttext), respond to the final inquiry. Information synthesis and mathematical analysis may be necessary. Incorporate insights from previous questions and answers in your response.",
        "Drawing upon the series of interconnected fiscal queries and the accompanying context from business financial statements (pretext, tables, and posttext), address the last question. This might require extracting relevant details and performing calculations. Integrate knowledge from preceding questions and their solutions in your reply.",
        "With reference to the linked set of finance-related questions and the supporting information from corporate economic filings (pretext, tables, and posttext), provide an answer to the ultimate query. Data extraction and arithmetic operations may be needed. Factor in the content of earlier questions and their answers when formulating your response.",
        "Considering the progression of interrelated financial inquiries and the background provided by company fiscal reports (including pretext, tables, and posttext), tackle the final question. This may involve information extraction and mathematical processing. Leverage insights from previous questions and their responses in crafting your answer."
    ]
}

SM_PROMPTS = {
    "template":
    [
        "Based on the provided data and tweets, predict whether the closing price of {stock} will increase or decrease at {date}. Answer only with Rise or Fall.",
        "Using the given information and social media posts, forecast if the closing price of {stock} will go up or down at {date}. Respond strictly with Rise or Fall.",
        "Analyze the supplied data and tweets to determine if the closing price of {stock} will advance or retreat at {date}. Please indicate either Rise or Fall.",
        "Considering the presented data and tweets, project whether the closing price of {stock} will appreciate or depreciate at {date}. Specify only Rise or Fall.",
        "Evaluate the given data and tweets to anticipate if the closing price of {stock} will climb or descend at {date}. Your response should be either Rise or Fall."
    ]
}

class fairevalEngine():

    def __init__(self, prompt_mapping, prompt_categories = 0, clean_text_type = None):
        self.prompt_mapping = prompt_mapping
        self.prompt_categories = prompt_categories
        self.clean_text_type = clean_text_type

    def randomise_prompt(self, doc):
        prompt = random.choice(self.prompt_mapping["template"])
        for category in range(self.prompt_categories):
            prompt = random.choice(self.prompt_mapping["template"])
            category_mapping = self.prompt_mapping[category]
            replacements = {}
            for k in category_mapping.keys():
                if k in doc["query"]:
                    replacements[f"category_{category}"] = random.choice(category_mapping[k])
                else:
                    raise ValueError("Invalid prompt format")
            prompt = prompt.format(**replacements)
        return prompt
    
    def clean_text(self, doc):
        if self.clean_text_type == 'text':
            return " Text: " + doc['text']
        elif self.clean_text_type == 'context':
            return " Context: " +doc['text']
        elif self.clean_text_type == "headlines":
            try:
                text = doc['query'].split("Text: ")[1].replace("Answer:","")
                return " Text: " + text
            except:
                raise ValueError("Invalid query format")
        elif self.clean_text_type == "finqa":
            try:
                context = doc['query'].split("Context: ")[1].split(" Question:")[0]
                question = doc['query'].split(" Question: ")[1].split(" Answer: ")[0]
                return " Context: " + context + " Question: " + question
            except:
                raise ValueError("Invalid query format")
        elif self.clean_text_type == "convfinqa":
            try:
                context = doc['query'].split("Context: ")[1].split(" Conversations:")[0]
                conversations = doc['query'].split(" Conversations: ")[1].split(" Answer: ")[0]
                return " Context: " + context + " Conversations: " + conversations
            except:
                raise ValueError("Invalid query format")
            
        elif self.clean_text_type == "sm":

    def doc_to_text(self, doc, answer_phrase = " Answer:"):
        return self.randomise_prompt(self.prompt_mapping, doc) + self.clean_text(doc) + answer_phrase