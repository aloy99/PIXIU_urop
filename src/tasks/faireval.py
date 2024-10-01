import random
import re
import logging

logger = logging.getLogger(__name__)

FPB_PROMPTS = {
    "template": [
        "Evaluate the sentiment in this excerpt from a financial news report. Classify the sentiment as positive, negative, or neutral.",
        "Determine the sentiment of this financial journalism snippet. Categorize the sentiment as neutral, positive, or negative.",
        "Interpret the sentiment in this extract from a piece of financial news. Label the sentiment as negative, neutral, or positive.",
        "Assess the sentiment in this financial news excerpt. Judge the sentiment as positive, neutral, or negative.",
        "Examine the sentiment of this financial news snippet. Analyse the sentiment as neutral, negative, or positive.",
        "Gauge the sentiment of this financial news excerpt, classifying it as negative, positive, or neutral.",
        "Categorize the sentiment in this statement from a financial article as negative, positive, or neutral.",
        "Identify the underlying sentiment in this financial news snippet, labeling it as negative, positive, or neutral.",
        "Discern the sentiment of this financial news quote, indicating whether it's negative, positive, or neutral.",
        "Pinpoint the sentiment expressed in this financial article extract, characterizing it as negative, positive, or neutral.",
        "Gauge the sentiment behind this financial news extract. Respond with a classification of negative, positive, or neutral.",
        "Review the sentiment of this financial journalism excerpt. Categorize your findings as negative, positive, or neutral.",
        "Decipher the sentiment in this statement from a finance article. Label it as negative, positive, or neutral.",
        "Parse the sentiment contained within this financial news passage. Designate it as negative, positive, or neutral.",
        "Scrutinize the sentiment of this finance-related news extract. Identify it as negative, positive, or neutral.",
        "Analyze the sentiment in this financial news passage, classifying them as negative, positive, or neutral.",
        "Unpack the sentiment conveyed by this finance-related news snippet, labeling it negative, positive, or neutral.",
        "Decode the sentiment of this financial journalism excerpt, categorizing it as negative, positive, or neutral.",
        "Break down the sentiment expressed in this financial article sample, designating it negative, positive, or neutral.",
        "Distill the sentiment from this financial news fragment, identifying it as negative, positive, or neutral.",
    ]
}

FIQASA_PROMPTS = {
    "template": [
        "Analyze the sentiment of this financial {category_0}. Classify the sentiment as Positive, Negative, or Neutral.",
        "Evaluate the sentiment in the given financial {category_0}. Categorize the sentiment as Positive, Negative, or Neutral.",
        "Determine the sentiment in this financial {category_0}. Label the sentiment as Positive, Negative, or Neutral.",
        "Assess the sentiment of the presented financial {category_0}. Judge the sentiment as Positive, Negative, or Neutral.",
        "Interpret the sentiment of the following financial {category_0}. Analyse the sentiment as Positive, Negative, or Neutral."
        "Classify the sentiment of the following financial {category_0} as either Positive, Negative, or Neutral.",
        "Identify the sentiment in this financial {category_0}: Is it Positive, Negative, or Neutral?",
        "Gauge the sentiment of the provided financial {category_0}: Positive, Negative, or Neutral?",
        "Categorize the sentiment of this financial {category_0} as Positive, Negative, or Neutral.",
        "Discern the sentiment within the following financial {category_0}: Positive, Negative, or Neutral?",
        "Label the sentiment of the given financial {category_0} as Positive, Negative, or Neutral.",
        "Characterize the sentiment expressed in this financial {category_0}: Positive, Negative, or Neutral?",
        "Examine the sentiment of the following financial {category_0} and indicate if it's Positive, Negative, or Neutral.",
        "Rate the sentiment of this financial {category_0}: Does it fall under Positive, Negative, or Neutral?",
        "Deduce the sentiment from the provided financial {category_0}: Positive, Negative, or Neutral?",
        "Decode the emotional tone of this financial {category_0}: Is it Positive, Negative, or Neutral?",
        "Pinpoint the sentiment conveyed in the given financial {category_0}: Positive, Negative, or Neutral?",
        "Unpack the sentiment behind this financial {category_0}, classifying it as Positive, Negative, or Neutral.",
        "Distill the sentiment from the presented financial {category_0} into Positive, Negative, or Neutral.",
        "Extract the underlying sentiment of this financial {category_0}, tagging it as Positive, Negative, or Neutral.",
    ],
    0: {
        "post": [
            "post",
        ],
        "headline": ["headline"],
    },
}

NER_PROMPTS = {
    "template": [
        "In the text snippets taken from financial agreements in United States Securities and Exchange Commission documents, detect entities categorized as individuals ('PER'), companies ('ORG'), or places ('LOC'). Present results as: 'entity name, entity type'.",
        "Locate and classify named entities within excerpts from financial agreements found in SEC filings. Identify persons ('PER'), organizations ('ORG'), and locations ('LOC'). Format your response as: 'entity name, entity type'.",
        "Analyze passages from financial contracts submitted to the U.S. SEC. Pinpoint entities that are people ('PER'), institutions ('ORG'), or geographical areas ('LOC'). List findings as: 'entity name, entity type'.",
        "Extract and categorize named entities from financial agreement segments in Securities and Exchange Commission reports. Tag humans ('PER'), groups ('ORG'), and sites ('LOC'). Output should be: 'entity name, entity type'.",
        "Within financial contract excerpts from SEC-filed documents, recognize entities representing individuals ('PER'), corporations ('ORG'), or territories ('LOC'). Structure answers as: 'entity name, entity type'.",
    ]
}

HEADLINE_PROMPTS = {
    "template": [
        "Is {category_0} a topic covered in the news headline? Respond with either Yes or No.",
        "Does the news headline address {category_0}? Your answer should be only Yes or No.",
        "Can information about {category_0} be found in the news headline? Reply with Yes or No only.",
        "Evaluate if the news headline contains information about {category_0}. Provide a Yes or No response.",
        "Determine whether {category_0} is referenced in the news headline. Answer exclusively with Yes or No.",
        "Is a gold-related {category_0} evident in the news headline? Answer with Yes or No.",
        "Can you spot a {category_0} concerning gold within the news headline? Respond Yes or No.",
        "Does the headline indicate a {category_0} involving gold? Reply with Yes or No.",
        "Is there any hint of a gold {category_0} in the news headline? Answer Yes or No.",
        "Are there signs of a {category_0} linked to gold in the headline? Respond Yes or No.",
        "Can a gold-associated {category_0} be detected in the news headline? Say Yes or No.",
        "Does the headline allude to a {category_0} in the gold market? Answer Yes or No.",
        "Is a {category_0} pertaining to gold present in the news headline? Respond with Yes or No.",
        "Can you find any mention of a gold-related {category_0} in the headline? Reply Yes or No.",
        "Does the news headline point to a {category_0} in gold? Answer Yes or No.",
        "Is there evidence of a gold {category_0} within the headline? Respond Yes or No.",
        "Can you identify a {category_0} connected to gold in the news headline? Say Yes or No.",
        "Does the headline suggest any {category_0} activity in gold? Answer with Yes or No.",
        "Is a {category_0} regarding gold noticeable in the news headline? Reply Yes or No.",
        "Can you discern a gold-specific {category_0} from the headline? Respond Yes or No.",
    ],
    0: {
        "Price or Not": ["price"],
        "Direction Up": ["price going up"],
        "Direction Constant": ["price staying constant"],
        "Direction Down": ["price going down"],
        "PastPrice": ["price in the past"],
        "FuturePrice": ["price in the future"],
        "PastNews": ["a general event (apart from prices) in the past"],
        "FutureNews": ["a general event (apart from prices) in the future"],
        "Asset Comparision": ["comparison of gold with any other asset"],
    },
}

FINQA_PROMPTS = {
    "template": [
        "Using the provided context, respond to the presented financial inquiry.",
        "Address the given financial question using the provided context.",
        "Based on the supplied context, offer an answer to the specified financial query.",
        "Referring to the contextual details, tackle the stated financial question.",
        "Utilize the given context to formulate a response to the posed financial inquiry.",
        "Drawing from the context provided, resolve the financial question at hand.",
        "Analyze the given context to answer the financial question presented.",
        "Use the contextual information to craft a response to the financial query.",
        "Considering the provided context, address the financial question posed.",
        "Examine the context and respond to the financial question accordingly.",
        "With the given context as a guide, answer the financial question presented.",
        "Leverage the provided context to tackle the financial inquiry at hand.",
        "Apply the contextual information to respond to the given financial question.",
        "In light of the supplied context, address the financial query presented.",
        "Process the given context to formulate an answer to the financial question.",
        "Interpret the provided context to respond to the financial inquiry posed.",
        "Using the contextual details given, offer insight into the financial question.",
        "Extract relevant information from the context to answer the financial query.",
        "Synthesize the provided context to address the financial question at hand.",
        "Derive an answer to the financial question based on the given contextual information.",
    ]
}

CONVFINQA_PROMPTS = {
    "template": [
        "Based on the sequence of linked financial inquiries and the supplementary details given in the pretext, tables, and posttext from corporate fiscal reports, answer the concluding question. This may involve data extraction and numerical computations. Consider all prior questions and their responses when crafting your answer.",
        "Utilizing the chain of related financial questions and the contextual data from company monetary documents (including pretext, tables, and posttext), respond to the final inquiry. Information synthesis and mathematical analysis may be necessary. Incorporate insights from previous questions and answers in your response.",
        "Drawing upon the series of interconnected fiscal queries and the accompanying context from business financial statements (pretext, tables, and posttext), address the last question. This might require extracting relevant details and performing calculations. Integrate knowledge from preceding questions and their solutions in your reply.",
        "With reference to the linked set of finance-related questions and the supporting information from corporate economic filings (pretext, tables, and posttext), provide an answer to the ultimate query. Data extraction and arithmetic operations may be needed. Factor in the content of earlier questions and their answers when formulating your response.",
        "Considering the progression of interrelated financial inquiries and the background provided by company fiscal reports (including pretext, tables, and posttext), tackle the final question. This may involve information extraction and mathematical processing. Leverage insights from previous questions and their responses in crafting your answer.",
        "Analyze the chain of finance-related queries, along with the pretext, tables, and posttext from corporate fiscal data, to answer the concluding question. Extract relevant information, perform calculations as needed, and consider prior questions and answers in your response.",
        "Synthesize the sequence of financial inquiries and the provided company monetary context (including pretext, tables, and posttext) to address the final query. This may involve data interpretation and numerical analysis. Incorporate insights from previous questions in your answer.",
        "Evaluate the series of linked fiscal questions alongside the given corporate financial details (pretext, tables, and posttext) to respond to the ultimate inquiry. Extract pertinent information, calculate if necessary, and integrate knowledge from preceding questions.",
        "Interpret the progression of interrelated financial queries and the accompanying business economic data (pretext, tables, and posttext) to tackle the last question. This might require information extraction and mathematical operations. Build upon earlier questions and answers in your response.",
        "Assess the connected set of finance-related questions and the supporting corporate monetary context (pretext, tables, and posttext) to formulate an answer to the final inquiry. Extract relevant data, perform calculations where needed, and consider prior questions in your reply.",
        "Examine the sequence of fiscal inquiries and the provided company financial information (including pretext, tables, and posttext) to address the concluding question. This may involve data analysis and arithmetic operations. Incorporate insights from previous questions and answers.",
        "Process the chain of interconnected financial queries and the supplementary corporate economic details (pretext, tables, and posttext) to respond to the ultimate question. Extract relevant information, calculate as necessary, and build upon prior inquiries in your answer.",
        "Dissect the series of linked finance-related questions and the given business fiscal context (pretext, tables, and posttext) to tackle the final inquiry. This might require data extraction and mathematical analysis. Consider preceding questions and their responses in your reply.",
        "Scrutinize the progression of interrelated monetary queries and the provided company financial data (pretext, tables, and posttext) to address the concluding question. Extract pertinent information, perform calculations if needed, and integrate insights from earlier questions.",
        "Analyze the sequence of connected fiscal inquiries and the accompanying corporate economic context (pretext, tables, and posttext) to formulate a response to the last question. This may involve information synthesis and numerical computations. Build upon previous questions and answers.",
        "Evaluate the chain of linked financial questions and the given business monetary details (including pretext, tables, and posttext) to answer the ultimate query. Extract relevant data, calculate where necessary, and consider prior inquiries in your response.",
        "Interpret the series of interrelated finance-related questions and the provided company fiscal information (pretext, tables, and posttext) to address the final inquiry. This might require data analysis and arithmetic operations. Incorporate insights from preceding questions.",
        "Assess the progression of connected economic queries and the supplementary corporate financial context (pretext, tables, and posttext) to tackle the concluding question. Extract pertinent information, perform calculations as needed, and build upon earlier questions and answers.",
        "Examine the sequence of linked monetary inquiries and the given business fiscal details (pretext, tables, and posttext) to respond to the ultimate question. This may involve information extraction and mathematical analysis. Consider prior questions in your reply.",
        "Dissect the chain of interconnected financial queries and the provided company economic data (including pretext, tables, and posttext) to formulate an answer to the last inquiry. Extract relevant information, calculate if necessary, and integrate insights from preceding questions and their responses.",
    ]
}

SM_PROMPTS = {
    "template": [
        "Based on the provided data and tweets, predict whether the closing price of {stock} will increase or decrease at {date}. Answer only with Rise or Fall.",
        "Using the given information and social media posts, forecast if the closing price of {stock} will go up or down at {date}. Respond strictly with Rise or Fall.",
        "Analyze the supplied data and tweets to determine if the closing price of {stock} will go up or down at {date}. Please indicate either Rise or Fall.",
        "Considering the presented data and tweets, project whether the closing price of {stock} will increase or decrease at {date}. Specify only Rise or Fall.",
        "Evaluate the given data and tweets to anticipate if the closing price of {stock} will rise or fall at {date}. Your response should be either Rise or Fall.",
        "Based on the data and tweets, predict if the closing price of {stock} will increase or decrease at {date}. Answer with Rise or Fall.",
        "Using the provided data and tweets, forecast whether {stock}'s closing price will go up or down at {date}. Respond with Rise or Fall.",
        "Analyze the given data and tweets to determine if the closing price of {stock} will rise or fall at {date}. Please answer Rise or Fall.",
        "Considering the data and tweets, project if the closing price of {stock} will increase or decrease at {date}. Indicate either Rise or Fall.",
        "Evaluate the data and tweets to anticipate whether the closing price of {stock} will go up or down at {date}. Reply with Rise or Fall.",
        "From the available data and tweets, predict if {stock}'s closing price will rise or fall at {date}. Respond only with Rise or Fall.",
        "Examine the data and tweets to forecast whether {stock}'s closing price will increase or decrease at {date}. Answer Rise or Fall.",
        "Review the provided data and tweets to determine if {stock}'s closing price will go up or down at {date}. Please state Rise or Fall.",
        "Assess the data and tweets to predict whether {stock}'s closing price will rise or fall at {date}. Respond with Rise or Fall.",
        "Based on the given data and tweets, anticipate if the closing price of {stock} will increase or decrease at {date}. Answer only Rise or Fall.",
        "Analyze the data and tweets to project whether {stock}'s closing price will go up or down at {date}. Please respond with Rise or Fall.",
        "Using the data and tweets provided, forecast if the closing price of {stock} will rise or fall at {date}. Indicate either Rise or Fall.",
        "Consider the data and tweets to predict whether {stock}'s closing price will increase or decrease at {date}. Reply with Rise or Fall.",
        "Evaluate the given data and tweets to determine if the closing price of {stock} will go up or down at {date}. Answer only Rise or Fall.",
        "From the data and tweets, anticipate whether {stock}'s closing price will rise or fall at {date}. Respond with Rise or Fall.",
    ]
}


class FairevalEngine:

    def __init__(
        self, prompt_mapping, prompt_categories=0, task_type=None, prompt_mode="random"
    ):
        self.prompt_mapping = prompt_mapping
        self.prompt_categories = prompt_categories
        self.task_type = task_type
        self.prompt_mode = prompt_mode

    def randomise_prompt(self, doc):
        prompt = random.choice(self.prompt_mapping["template"])
        for category in range(self.prompt_categories):
            prompt = random.choice(self.prompt_mapping["template"])
            category_mapping = self.prompt_mapping[category]
            replacements = {}
            for k in category_mapping.keys():
                if k in doc["query"]:
                    replacements[f"category_{category}"] = random.choice(
                        category_mapping[k]
                    )
            if f"category_{category}" not in replacements:
                logger.info(doc["query"])
                raise ValueError("Invalid prompt format")
            prompt = prompt.format(**replacements)
        if self.task_type == "sm":
            stock = re.search(r"closing price of (.*?) ", doc["query"]).group(1)
            date = re.search(r"at (.*?)[\?.]", doc["query"]).group(1)
            prompt = prompt.format(stock=stock, date=date)
        return prompt

    def test_docs(self):
        if self.prompt_mode == "random":
            return super().test_docs()
        elif self.prompt_mode == "all":
            return self.test_docs() * len(self.prompt_mapping["template"])

    def clean_text(self, doc):
        if self.task_type == "text":
            return " Text: " + doc["text"]
        elif self.task_type in ["context", "sm"]:
            return " Context: " + doc["text"]
        elif self.task_type == "headlines":
            try:
                text = doc["query"].split("Text: ")[1].replace("Answer:", "")
                return " Text: " + text
            except:
                logger.info(doc["query"])
                raise ValueError("Invalid query format")
        elif self.task_type == "finqa":
            try:
                context = doc["query"].split("Context:")[1].split("Question:")[0]
                question = doc["query"].split("Question:")[1].split("Answer:")[0]
                return " Context: " + context + " Question: " + question
            except:
                logger.info(doc["query"])
                raise ValueError("Invalid query format")
        elif self.task_type == "convfinqa":
            try:
                context = doc["query"].split("Context:")[1].split(" Conversations:")[0]
                conversations = (
                    doc["query"].split("Conversations:")[1].split("Answer:")[0]
                )
                return " Context: " + context + " Conversations: " + conversations
            except:
                logger.info(doc["query"])
                raise ValueError("Invalid query format")

        elif self.task_type == "sm":
            try:
                context = doc["query"].split("Context:")[1].split("Answer:")[0]
                return " Context: " + context
            except:
                logger.info(doc["query"])
                raise ValueError("Invalid query format")

    def doc_to_text(self, doc, answer_phrase=" Answer:"):
        return self.randomise_prompt(doc) + self.clean_text(doc) + answer_phrase

    def get_prompt_count(self):
        return len(self.prompt_mapping["template"])
