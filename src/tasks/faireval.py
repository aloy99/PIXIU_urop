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
        "Using a category of negative, positive, or neutral, categorize the sentiment in this statement from a financial article.",
        "Identify the sentiment in this financial news snippet, labeling it as negative, positive, or neutral.",
        "Discern the sentiment of this financial news quote, indicating whether it's neutral, negative, or positive.",
        "Pinpoint the sentiment expressed in this financial article extract, characterizing it as positive, neutral, or negative.",
        "Using neutral, negative, or positive, gauge the sentiment behind this financial news extract.",
        "From the options of positive, neutral, or negative, review the sentiment of this financial journalism excerpt.",
        "Choosing from negative, positive, or neutral, decipher the sentiment in this statement from a finance article.",
        "Determine whether neutral, negative, or positive best describes the sentiment contained within this financial news passage.",
        "Considering positive, neutral, or negative classifications, scrutinize the sentiment of this finance-related news extract.",
        "Which of neutral, positive, or negative, is the appropriate classification for the sentiment in this financial news passage?",
        "Picking from negative, positive, or neutral, unpack the sentiment conveyed by this finance-related news snippet.",
        "Selecting one of positive, neutral, or negative, decode the sentiment of this financial journalism excerpt.",
        "With your options being neutral, negative, or positive, identify the sentiment expressed in this financial article sample.",
        "Select one of positive, negative, or neutral to label the sentiment from this financial news fragment."
    ]
}

FIQASA_PROMPTS = {
    "template": [
        "Evaluate the sentiment in this financial {category_0}. Classify the sentiment as positive, negative, or neutral.",
        "Determine the sentiment of this financial {category_0}. Categorize the sentiment as neutral, positive, or negative.",
        "Interpret the sentiment in this extract from a financial {category_0}. Label the sentiment as negative, neutral, or positive.",
        "Assess the sentiment in this financial {category_0}. Judge the sentiment as positive, neutral, or negative.",
        "Examine the sentiment of this financial {category_0}. Analyse the sentiment as neutral, negative, or positive.",
        "Gauge the sentiment of this financial {category_0}, classifying it as negative, positive, or neutral.",
        "Using a category of negative, positive, or neutral, categorize the sentiment in this statement from a financial {category_0}.",
        "Identify the sentiment in this financial {category_0}, labeling it as negative, positive, or neutral.",
        "Discern the sentiment of this financial {category_0}, indicating whether it's neutral, negative, or positive.",
        "Pinpoint the sentiment expressed in this financial {category_0}, characterizing it as positive, neutral, or negative.",
        "Using neutral, negative, or positive, gauge the sentiment behind this financial {category_0}.",
        "From the options of positive, neutral, or negative, review the sentiment of this financial {category_0}.",
        "Choosing from negative, positive, or neutral, decipher the sentiment in this statement from a financial {category_0}.",
        "Determine whether neutral, negative, or positive best describes the sentiment contained within this financial {category_0}.",
        "Considering positive, neutral, or negative classifications, scrutinize the sentiment of this financial {category_0}.",
        "Which of neutral, positive, or negative is the appropriate classification for the sentiment in this financial {category_0}?",
        "Picking from negative, positive, or neutral, unpack the sentiment conveyed by this financial {category_0}.",
        "Selecting one of positive, neutral, or negative, decode the sentiment of this financial {category_0}.",
        "With your options being neutral, negative, or positive, identify the sentiment expressed in this financial {category_0}.",
        "Select one of positive, negative, or neutral to label the sentiment from this financial {category_0}."
    ]
,
    0: {
        "post": [
            "post",
        ],
        "headline": ["headline"],
    },
}

NER_PROMPTS = {
    "template": [
        "In the text snippets taken from financial agreements in United States Securities and Exchange Commission documents, detect entities categorized as organizations ('ORG'), locations ('LOC'), or persons ('PER'). Present results as: 'entity name, entity type'.",
        "Locate and classify named entities within excerpts from financial agreements found in SEC filings. Identify the entities as locations ('LOC'), persons ('PER'), or organizations ('ORG'). Format your response as: 'entity name, entity type'.",
        "Analyze passages from financial contracts submitted to the U.S. SEC. Pinpoint entities that are persons ('PER'), locations ('LOC'), or organizations ('ORG'). List findings as: 'entity name, entity type'.",
        "Extract and categorize named entities from financial agreement segments in Securities and Exchange Commission reports. Tag locations ('LOC'), persons ('PER'), or organizations ('ORG'). Output should be: 'entity name, entity type'.",
        "Within financial contract excerpts from SEC-filed documents, recognize entities representing organizations ('ORG'), persons ('PER'), or locations ('LOC'). Structure answers as: 'entity name, entity type'.",
        "Analyze sentences from U.S. SEC filing financial agreements to detect named entities representing an organization ('ORG'), a location ('LOC'), or a person ('PER'). Present findings as: 'entity name, entity type'.",
        "Examine financial agreement text extracted from SEC filings in the United States to pinpoint named entities categorized as a location ('LOC'), a person ('PER'), or an organization ('ORG'). Output should be: 'entity name, entity type'.",
        "Within financial agreement excerpts from U.S. Securities and Exchange Commission documents, locate and classify named entities as a person ('PER'), a location ('LOC'), or an organization ('ORG'). Format answers as: 'entity name, entity type'.",
        "Scrutinize sentences taken from U.S. SEC filing financial contracts to isolate named entities falling under the categories of an organization ('ORG'), a person ('PER'), or a location ('LOC'). Provide results in the format: 'entity name, entity type'.",
        "In financial agreement text sourced from SEC filings in the U.S., spot and tag named entities that qualify as a location ('LOC'), a person ('PER'), or an organization ('ORG'). Present findings as: 'entity name, entity type'.",
        "Parse through sentences extracted from U.S. Securities and Exchange Commission financial agreements to recognize named entities classified as an organization ('ORG'), a location ('LOC'), or a person ('PER'). List results as: 'entity name, entity type'.",
        "From financial agreement sentences in United States SEC filings, extract and categorize named entities representing a person ('PER'), a location ('LOC'), or an organization ('ORG'). Format output as: 'entity name, entity type'.",
        "Comb through U.S. SEC filing financial agreement text to identify named entities that fall into the categories of a location ('LOC'), an organization ('ORG'), or a person ('PER'). Present findings in the format: 'entity name, entity type'.",
        "Survey sentences from financial agreements found in U.S. Securities and Exchange Commission filings, highlighting named entities that represent an organization ('ORG'), a location ('LOC'), or a person ('PER'). The output should be: 'entity name, entity type'.",
        "In financial agreement excerpts from U.S. SEC documents, detect and label named entities that correspond to a location ('LOC'), a person ('PER'), or an organization ('ORG'). Provide answers as: 'entity name, entity type'.",
        "Scan sentences drawn from U.S. SEC financial agreements to spot named entities that qualify as a location ('LOC'), a person ('PER'), or an organization ('ORG'). Present results in the format: 'entity name, entity type'.",
        "Within financial contract text from United States Securities and Exchange Commission filings, pinpoint named entities categorized as an organization ('ORG'), a location ('LOC'), or a person ('PER'). List findings as: 'entity name, entity type'.",
        "Analyze financial agreement sentences extracted from U.S. SEC documents to identify and classify named entities as a location ('LOC'), a person ('PER'), or an organization ('ORG'). Format responses as: 'entity name, entity type'.",
        "Examine text from financial agreements in United States Securities and Exchange Commission filings, isolating named entities that represent a person ('PER'), an organization ('ORG'), or a location ('LOC'). Provide the output in the form: 'entity name, entity type'.",
        "In sentences culled from U.S. SEC filing financial agreements, locate and tag named entities falling under the categories of an organization ('ORG'), a location ('LOC'), or a person ('PER'). Present results as: 'entity name, entity type'."
    ]
}

HEADLINE_PROMPTS = {
    "template": [
        "Is {category_0} a topic covered in the news headline? Respond with either Yes or No.",
        "Answering with only Yes or No, does the news headline address {category_0}?",
        "Reply with Yes or No only. Can information about {category_0} be found in the news headline?",
        "Evaluate if the news headline contains information about {category_0}. Provide a Yes or No response.",
        "Determine whether {category_0} is referenced in the news headline. Answer exclusively with Yes or No.",
        "Answer with Yes or No. Is a gold-related {category_0} evident in the news headline?",
        "Respond with Yes or No. Can you spot a {category_0} concerning gold within the news headline?",
        "Does the headline indicate a {category_0} involving gold? Reply with Yes or No.",
        "Is there any hint of a gold {category_0} in the news headline? Answer Yes or No.",
        "Respond with Yes or No. Are there signs of a {category_0} linked to gold in the headline?",
        "Only respond with Yes or No. Can a gold-associated {category_0} be detected in the news headline?",
        "Answer with Yes or No. Does the headline allude to a {category_0} in the gold market?",
        "Is a {category_0} pertaining to gold present in the news headline? Respond with Yes or No.",
        "Replying with Yes or No, can you find any mention of a gold-related {category_0} in the headline?",
        "Does the news headline point to a {category_0} in gold? Answer Yes or No.",
        "Is there evidence of a gold {category_0} within the headline? Respond Yes or No.",
        "Answer the question with Yes or No. Can you identify a {category_0} connected to gold in the news headline?",
        "Does the headline suggest any {category_0} activity in gold? Answer with Yes or No.",
        "Reply Yes or No. Is a {category_0} regarding gold noticeable in the news headline? ",
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
        "Formulate a response to the posed financial inquiry, utilizing the given context   .",
        "Resolve the financial question at hand by drawing from the context provided.",
        "Analyze the given context to answer the financial question presented.",
        "Craft a response to the financial query using the contextual information.",
        "Address the financial question posed, considering the provided context,",
        "Examine the context and respond to the financial question accordingly.",
        "With the given context as a guide, answer the financial question presented.",
        "Leverage the provided context to tackle the financial inquiry at hand.",
        "Apply the contextual information to respond to the given financial question.",
        "Address the financial query presented in light of the supplied context.",
        "Process the given context to formulate an answer to the financial question.",
        "Respond to the financial inquiry posed by interpreting the provided context.",
        "Answer the financial question using the contextual details given.",
        "Extract relevant information from the context to answer the financial query.",
        "Address the financial question at hand through synthesizing the provided context.",
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
        "Answer only with Fall or Rise. Based on the provided data and tweets, predict whether the closing price of {stock} will fall or rise at {date}.",
        "Using the given information and social media posts, forecast if the closing price of {stock} will rise or fall at {date}. Respond strictly with Rise or Fall.",
        "Please indicate either Fall or Rise. Analyze the supplied data and tweets to determine if the closing price of {stock} will fall or rise at {date}.",
        "Specify only Rise or Fall. Considering the presented data and tweets, project whether the closing price of {stock} will rise or fall at {date}.",
        "Your response should be either Rise or Fall. Evaluate the given data and tweets to anticipate if the closing price of {stock} will rise or fall at {date}.",
        "Based on the data and tweets, predict if the closing price of {stock} will fall or rise at {date}. Answer with Fall or Rise.",
        "Respond with Rise or Fall. Using the provided data and tweets, forecast whether {stock}'s closing price will rise or fall at {date}.",
        "Please answer Fall or Rise. Analyze the given data and tweets to determine if the closing price of {stock} will fall or rise at {date}.",
        "Considering the data and tweets, project if the closing price of {stock} will rise or fall at {date}. Indicate either Rise or Fall.",
        "Reply with Fall or Rise. Evaluate the data and tweets to anticipate whether the closing price of {stock} will fall or rise at {date}.",
        "From the available data and tweets, predict if {stock}'s closing price will rise or fall at {date}. Respond only with Rise or Fall.",
        "Answer Fall or Rise. Examine the data and tweets to forecast whether {stock}'s closing price will fall or rise at {date}.",
        "Review the provided data and tweets to determine if {stock}'s closing price will rise or fall at {date}. Please state Rise or Fall.",
        "Respond with Fall or Rise. Assess the data and tweets to predict whether {stock}'s closing price will fall or rise at {date}.",
        "Answer only Rise or Fall. Based on the given data and tweets, anticipate if the closing price of {stock} will rise or fall at {date}.",
        "Analyze the data and tweets to project whether {stock}'s closing price will fall or rise at {date}. Please respond with Fall or Rise.",
        "Using the data and tweets provided, forecast if the closing price of {stock} will rise or fall at {date}. Indicate either Rise or Fall.",
        "Consider the data and tweets to predict whether {stock}'s closing price will fall or rise at {date}. Reply with Fall or Rise.",
        "Evaluate the given data and tweets to determine if the closing price of {stock} will rise or fall at {date}. Answer only Rise or Fall.",
        "From the data and tweets, anticipate whether {stock}'s closing price will fall or rise at {date}. Respond with Fall or Rise."
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
        self.set_prompt_index = None

    def randomise_prompt(self, doc):
        if self.set_prompt_index:
            prompt = self.prompt_mapping["template"][self.set_prompt_index]
        else:
            prompt = random.choice(self.prompt_mapping["template"])
        for category in range(self.prompt_categories):
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

    def set_prompt(self, prompt_index):
        self.set_prompt_index = prompt_index

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
