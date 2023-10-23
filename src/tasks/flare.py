"""
FLARE
"""
from lm_eval.base import Task, rf
from lm_eval.metrics import mean
import numpy as np
from .utils import process_text
from .zhutils import process_zhtext
from seqeval.metrics import f1_score as entity_score
from sklearn.metrics import f1_score, matthews_corrcoef
from bart_score import BARTScorer
import evaluate

_CITATION = """
@misc{xie2023pixiu,
      title={PIXIU: A Large Language Model, Instruction Data and Evaluation Benchmark for Finance}, 
      author={Qianqian Xie and Weiguang Han and Xiao Zhang and Yanzhao Lai and Min Peng and Alejandro Lopez-Lira and Jimin Huang},
      year={2023},
      eprint={2306.05443},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""


class Classification(Task):
    CALCULATE_MCC = False
    LOWER_CASE = True
    VERSION = 1
    EVAL_LAST_TURN = True

    def reformulate_turn_req(self, req, turn_request, turn):
        return req

    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return True

    def training_docs(self):
        return self.dataset["train"]

    def validation_docs(self):
        return self.dataset["validation"]

    def test_docs(self):
        return self.dataset["test"]

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        cont_request = rf.greedy_until(ctx, {"until": None})
        return cont_request

    def doc_to_decontamination_query(self, doc):
        return doc["text"]

    def doc_to_text(self, doc):
        # TODO: Format the query prompt portion of the document example.
        return doc["query"]

    def doc_to_target(self, doc):
        # TODO: Format the query prompt portion of the document example.
        return doc["answer"]

    def process_results(self, doc, results):
        gold: str = doc["choices"][doc["gold"]]
        if self.LOWER_CASE:
            gold = gold.lower()
        ini_result = results[0].strip()
        if self.LOWER_CASE:
            ini_result = ini_result.lower()

        result = None
        for choice in doc["choices"]:
            if self.LOWER_CASE:
                choice = choice.lower()
            if choice in ini_result:
                result = choice
                break
        if result is None:
            result = "missing"

        acc = 1.0 if gold == result else 0.0

        results = {
            "acc": acc,
            "missing": int(result == "missing"),
            "f1": (result, gold),
            "macro_f1": (result, gold),
        }

        if self.CALCULATE_MCC:
            results["mcc"] = (result, gold)

        return results

    def higher_is_better(self):
        metrics = {
            "acc": True,
            "f1": True,
            "macro_f1": True,
            "missing": False,
        }
        if self.CALCULATE_MCC:
            metrics["mcc"] = True
        return metrics

    def weighted_f1(self, items):
        preds, golds = zip(*items)
        labels = list(set(golds))
        preds = np.array(preds)
        golds = np.array(golds)
        f1 = f1_score(golds, preds, average="weighted", labels=labels)
        return f1

    def macro_f1(self, items):
        preds, golds = zip(*items)
        labels = list(set(golds))
        preds = np.array(preds)
        golds = np.array(golds)
        f1 = f1_score(golds, preds, average="macro", labels=labels)
        return f1

    def matthews_corrcoef(self, items):
        preds, golds = zip(*items)
        labels = {label: i for i, label in enumerate(list(set(golds)))}
        preds = [labels.get(pred, -1) for pred in preds]
        golds = [labels.get(gold, -1) for gold in golds]
        return matthews_corrcoef(golds, preds)

    def aggregation(self):
        metrics = {
            "acc": mean,
            "missing": mean,
            "f1": self.weighted_f1,
            "macro_f1": self.macro_f1,
        }
        if self.CALCULATE_MCC:
            metrics["mcc"] = self.matthews_corrcoef
        return metrics


class SequentialLabeling(Task):
    VERSION = 1
    DATASET_NAME = None
    LMAP = {"O": 0}
    EVAL_LAST_TURN = True

    def reformulate_turn_req(self, req, turn_request, turn):
        return req

    def has_training_docs(self):
        return False

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True

    def training_docs(self):
        return self.dataset["train"]

    def validation_docs(self):
        return self.dataset["validation"]

    def test_docs(self):
        return self.dataset["test"]

    def doc_to_text(self, doc):
        # TODO: Format the query prompt portion of the document example.
        return doc["query"]

    def doc_to_target(self, doc):
        return "\nAnswer: " + doc["answer"]

    def process_results(self, doc, results):
        return {
            "entity_f1": (doc["label"], results[0], doc["token"]),
            "f1": (doc["label"], results[0], doc["token"]),
        }

    def higher_is_better(self):
        return {
            "f1": True,
            "entity_f1": True,
        }

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        cont_request = rf.greedy_until(ctx, {"until": None})
        return cont_request

    def process_result(self, pred, gold, tokens):
        format_pred = ["O"] * len(gold)
        for index, pre in enumerate(pred.split("\n")[: len(tokens)]):
            try:
                word, label = pre.split(":")
            except:
                continue
            if word == tokens[index] and label in self.LMAP.keys():
                format_pred[index] = label
        return format_pred

    def entity_f1(self, items):
        golds, preds, tokens = zip(*items)

        list_preds = [
            self.process_result(pred, gold, token)
            for pred, gold, token in zip(preds, golds, tokens)
        ]
        f1 = entity_score(golds, list_preds)
        return f1

    def process_label_result(self, pred, gold, tokens):
        format_pred = [-1] * len(gold)
        for index, pre in enumerate(pred.split("\n")[: len(tokens)]):
            try:
                word, label = pre.split(":")
            except:
                continue
            if word == tokens[index]:
                format_pred[index] = self.LMAP.get(label, -1)
        return format_pred

    def label_f1(self, items):
        golds, preds, tokens = zip(*items)

        list_preds = [
            self.process_label_result(pred, gold, token)
            for pred, gold, token in zip(preds, golds, tokens)
        ]
        list_preds = [item for sublist in list_preds for item in sublist]
        golds = [self.LMAP[item] for sublist in golds for item in sublist]
        f1 = f1_score(golds, list_preds, average="weighted")
        return f1

    def aggregation(self):
        return {
            "entity_f1": self.entity_f1,
            "f1": self.label_f1,
        }


class AbstractiveSummarization(Task):
    VERSION = 1
    DATASET_NAME = None
    EVAL_LAST_TURN = True

    def reformulate_turn_req(self, req, turn_request, turn):
        return req

    def has_training_docs(self):
        return False

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True

    def training_docs(self):
        return self.dataset["train"]

    def validation_docs(self):
        return self.dataset["validation"]

    def test_docs(self):
        return self.dataset["test"]

    def doc_to_text(self, doc):
        # TODO: Format the query prompt portion of the document example.
        return doc["query"]

    def doc_to_target(self, doc):
        return doc["answer"]

    def process_results(self, doc, results):
        return {
            "rouge1": (doc["answer"], results[0]),
            "rouge2": (doc["answer"], results[0]),
            "rougeL": (doc["answer"], results[0]),
            "bert_score_f1": (doc["answer"], results[0]),
            "bart_score": (doc["answer"], results[0]),
        }

    def higher_is_better(self):
        return {
            "rouge1": True,
            "rouge2": True,
            "rougeL": True,
            "bert_score_f1": True,
            "bart_score": True,
        }

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        cont_request = rf.greedy_until(ctx, {"until": None})
        return cont_request

    def rouge_score(self, items):
        golds, preds = zip(*items)
        rouge = evaluate.load("rouge")
        results = rouge.compute(predictions=preds, references=golds)
        return results

    def rouge1(self, items):
        results = self.rouge_score(items)
        return results["rouge1"]

    def rouge2(self, items):
        results = self.rouge_score(items)
        return results["rouge2"]

    def rougeL(self, items):
        results = self.rouge_score(items)
        return results["rougeL"]

    def bert_score(self, items):
        if getattr(self, "_cache_bertscore", None) is None:
            golds, preds = zip(*items)
            bertscore = evaluate.load("evaluate-metric/bertscore")
            self._cache_bertscore = bertscore.compute(
                predictions=preds,
                references=golds,
                model_type="bert-base-multilingual-cased",
            )
            return self._cache_bertscore
        else:
            return self._cache_bertscore

    def bert_score_f1(self, items):
        res = self.bert_score(items)
        return sum(res["f1"]) / len(res["f1"])

    def bart_score(self, items):
        golds, preds = zip(*items)
        bart_scorer = BARTScorer(device="cuda", checkpoint="facebook/bart-large-cnn")
        bart_scorer.load(path="src/metrics/BARTScore/bart_score.pth")
        res = bart_scorer.score(srcs=preds, tgts=golds, batch_size=8)
        return sum(res) / len(res)

    def aggregation(self):
        return {
            "rouge1": self.rouge1,
            "rouge2": self.rouge2,
            "rougeL": self.rougeL,
            "bert_score_f1": self.bert_score_f1,
            "bart_score": self.bart_score,
        }


class ExtractiveSummarization(Task):
    VERSION = 1
    DATASET_NAME = None
    EVAL_LAST_TURN = True

    def reformulate_turn_req(self, req, turn_request, turn):
        return req

    def has_training_docs(self):
        return False

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True

    def training_docs(self):
        return self.dataset["train"]

    def validation_docs(self):
        return self.dataset["validation"]

    def test_docs(self):
        return self.dataset["test"]

    def doc_to_text(self, doc):
        # TODO: Format the query prompt portion of the document example.
        return doc["query"]

    def doc_to_target(self, doc):
        return doc["answer"]

    def process_results(self, doc, results):
        return {
            "rouge1": (doc["label"], doc["text"], results[0]),
            "rouge2": (doc["label"], doc["text"], results[0]),
            "rougeL": (doc["label"], doc["text"], results[0]),
            "bert_score_f1": (doc["label"], doc["text"], results[0]),
            "bart_score": (doc["label"], doc["text"], results[0]),
        }

    def higher_is_better(self):
        return {
            "rouge1": True,
            "rouge2": True,
            "rougeL": True,
            "bert_score_f1": True,
            "bart_score": True,
        }

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        cont_request = rf.greedy_until(ctx, {"until": None})
        return cont_request

    def get_sum(self, labels, texts):
        summ = []
        for label, text in zip(labels, texts):
            text = text.split("\n")
            new_text = "\n".join(
                [
                    text[index]
                    for index in range(len(text))
                    if index < len(label) and label[index] == 1
                ]
            )
            summ.append(new_text)
        return summ

    def rouge_score(self, items):
        golds, texts, preds = zip(*items)
        golds = self.get_sum(golds, texts)
        preds = self.get_sum([val.split("\n") for val in preds], texts)
        rouge = evaluate.load("rouge")
        results = rouge.compute(predictions=preds, references=golds)
        return results

    def rouge1(self, items):
        results = self.rouge_score(items)
        return results["rouge1"]

    def rouge2(self, items):
        results = self.rouge_score(items)
        return results["rouge2"]

    def rougeL(self, items):
        results = self.rouge_score(items)
        return results["rougeL"]

    def bert_score(self, items):
        if getattr(self, "_cache_bertscore", None) is None:
            golds, texts, preds = zip(*items)
            golds = self.get_sum(golds, texts)
            preds = self.get_sum([val.split("\n") for val in preds], texts)

            bertscore = evaluate.load("evaluate-metric/bertscore")
            self._cache_bertscore = bertscore.compute(
                predictions=preds,
                references=golds,
                model_type="bert-base-multilingual-cased",
            )
            return self._cache_bertscore
        else:
            return self._cache_bertscore

    def bert_score_f1(self, items):
        res = self.bert_score(items)
        return sum(res["f1"]) / len(res["f1"])

    def bart_score(self, items):
        golds, texts, preds = zip(*items)
        golds = self.get_sum(golds, texts)
        preds = self.get_sum([val.split("\n") for val in preds], texts)

        bart_scorer = BARTScorer(device="cuda:0", checkpoint="facebook/bart-large-cnn")
        bart_scorer.load(path="src/metrics/BARTScore/bart_score.pth")
        res = bart_scorer.score(srcs=preds, tgts=golds, batch_size=8)
        return sum(res) / len(res)

    def aggregation(self):
        return {
            "rouge1": self.rouge1,
            "rouge2": self.rouge2,
            "rougeL": self.rougeL,
            "bert_score_f1": self.bert_score_f1,
            "bart_score": self.bart_score,
        }


class RelationExtraction(Task):
    VERSION = 1
    DATASET_NAME = None
    EVAL_LAST_TURN = True

    def reformulate_turn_req(self, req, turn_request, turn):
        return req

    def has_training_docs(self):
        return False

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True

    def training_docs(self):
        return self.dataset["train"]

    def validation_docs(self):
        return self.dataset["validation"]

    def test_docs(self):
        return self.dataset["test"]

    def doc_to_text(self, doc):
        # TODO: Format the query prompt portion of the document example.
        return doc["query"]

    def doc_to_target(self, doc):
        return doc["answer"]

    def process_results(self, doc, results):
        return {
            "precision": (doc["label"], results[0]),
            "recall": (doc["label"], results[0]),
            "f1": (doc["label"], results[0]),
        }

    def higher_is_better(self):
        return {
            "precision": True,
            "recall": True,
            "f1": True,
        }

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        cont_request = rf.greedy_until(ctx, {"until": None})
        return cont_request

    def process(self, items):
        golds, preds = zip(*items)

        all_golds = []
        all_preds = []

        for gold, pred in zip(golds, preds):
            all_golds.extend(gold)
            pred = pred.split("\n")
            all_preds.extend(pred)

        return set(all_golds), set(all_preds)

    def precision(self, items):
        golds, preds = self.process(items)
        tp = golds & preds
        prec = len(tp) / len(preds)
        return prec

    def recall(self, items):
        golds, preds = self.process(items)
        tp = golds & preds
        rec = len(tp) / len(golds)
        return rec

    def cal_f1(self, items):
        prec = self.precision(items)
        rec = self.recall(items)
        if prec + rec == 0.0:
            return 0.0
        return 2 * (prec * rec) / (prec + rec)

    def aggregation(self):
        return {
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.cal_f1,
        }


class QA(Task):
    VERSION = 1
    DATASET_NAME = None
    EVAL_LAST_TURN = True

    def reformulate_turn_req(self, req, turn_request, turn):
        return req

    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return True

    def training_docs(self):
        return self.dataset["train"]

    def validation_docs(self):
        return self.dataset["validation"]

    def test_docs(self):
        return self.dataset["test"]

    def should_decontaminate(self):
        return True

    def doc_to_decontamination_query(self, doc):
        return doc["text"]

    def doc_to_text(self, doc):
        # TODO: Format the query prompt portion of the document example.
        return doc["query"]

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        cont_request = rf.greedy_until(ctx, {"until": None})
        return cont_request

    def doc_to_target(self, doc):
        return doc["answer"]

    def process_results(self, doc, results):
        gold = doc["answer"]

        acc = 1.0 if results[0].strip() == gold else 0.0

        return {
            "acc": acc,
        }

    def higher_is_better(self):
        return {
            "acc": True,
        }

    def aggregation(self):
        return {
            "acc": mean,
        }


class FPB(Classification):
    DATASET_PATH = "chancefocus/flare-fpb"


class FIQASA(Classification):
    DATASET_PATH = "chancefocus/flare-fiqasa"


class NER(Task):
    VERSION = 1
    DATASET_PATH = "chancefocus/flare-ner"
    DATASET_NAME = None
    EVAL_LAST_TURN = True

    def reformulate_turn_req(self, req, turn_request, turn):
        return req

    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return True

    def training_docs(self):
        return self.dataset["train"]

    def validation_docs(self):
        return self.dataset["validation"]

    def test_docs(self):
        return self.dataset["test"]

    def should_decontaminate(self):
        return True

    def doc_to_decontamination_query(self, doc):
        return doc["text"]

    def doc_to_text(self, doc):
        # TODO: Format the query prompt portion of the document example.
        return doc["query"]

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        cont_request = rf.greedy_until(ctx, {"until": None})
        return cont_request

    def doc_to_target(self, doc):
        return doc["answer"]

    def process_results(self, doc, results):
        text = doc["text"]
        pred = process_text(results[0], text)

        return {"entity_f1": (pred, doc["label"], results[0])}

    def higher_is_better(self):
        return {
            "entity_f1": True,
        }

    @classmethod
    def entity_f1(cls, items):
        preds, golds, _ = zip(*items)
        f1 = entity_score(golds, preds)
        return f1

    def aggregation(self):
        return {
            "entity_f1": self.entity_f1,
        }


class FinQA(QA):
    DATASET_PATH = "chancefocus/flare-finqa"


class StockMovement(Classification):
    DATASET_NAME = None
    CALCULATE_MCC = True
    CHOICE_DICT = {
        "rise": ["yes", "positive"],
        "fall": ["no", "negative", "neutral"],
    }
    DEFAULT = "fall"

    def process_results(self, doc, results):
        gold: str = doc["choices"][doc["gold"]]
        if self.LOWER_CASE:
            gold = gold.lower()
        ini_result = results[0].strip()
        if self.LOWER_CASE:
            ini_result = ini_result.lower()

        result = None
        for choice in doc["choices"]:
            if self.LOWER_CASE:
                choice = choice.lower()
            if choice in ini_result or any(
                [val in ini_result for val in self.CHOICE_DICT[choice]]
            ):
                result = choice
                break
        if result is None:
            result = self.DEFAULT

        acc = 1.0 if gold == result else 0.0

        results = {
            "acc": acc,
            "missing": int(result == "missing"),
            "f1": (result, gold),
            "macro_f1": (result, gold),
        }

        if self.CALCULATE_MCC:
            results["mcc"] = (result, gold)

        return results


class StockMovementBigData(StockMovement):
    DATASET_PATH = "chancefocus/flare-sm-bigdata"


class StockMovementACL(StockMovement):
    DATASET_PATH = "chancefocus/flare-sm-acl"


class StockMovementCIKM(StockMovement):
    DATASET_PATH = "chancefocus/flare-sm-cikm"


SM_TASKS = {
    "flare_sm_bigdata": StockMovementBigData,
    "flare_sm_acl": StockMovementACL,
    "flare_sm_cikm": StockMovementCIKM,
}


class Headlines(Classification):
    DATASET_PATH = "chancefocus/flare-headlines"

    def process_results(self, doc, results):
        gold = doc["gold"]

        return {
            "avg_f1": (doc["label_type"], int(results[0].strip() != "Yes"), gold, results),
        }

    def higher_is_better(self):
        return {
            "avg_f1": True,
        }

    @classmethod
    def label_avg(cls, items):
        labels, preds, golds, rels = zip(*items)
        label_set = set(labels)
        labels = np.array(labels)
        preds = np.array(preds)
        golds = np.array(golds)
        all_f1s = []
        for l in label_set:
            pds = preds[labels == l]
            gds = golds[labels == l]
            f1 = f1_score(gds, pds, average="weighted", labels=[0, 1])
            all_f1s.append(f1)
        return np.mean(all_f1s)

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        cont_request = rf.greedy_until(ctx, {"until": None})
        return cont_request

    def aggregation(self):
        return {
            "avg_f1": self.label_avg,
        }


class FinerOrd(SequentialLabeling):
    DATASET_PATH = "chancefocus/flare-finer-ord"
    LMAP = {
        "O": 0,
        "B-PER": 1,
        "I-PER": 2,
        "B-LOC": 3,
        "I-LOC": 4,
        "B-ORG": 5,
        "I-ORG": 6,
    }


class FOMC(Classification):
    DATASET_PATH = "chancefocus/flare-fomc"


class German(StockMovement):
    DATASET_PATH = "chancefocus/flare-german"
    CHOICE_DICT = {
        "good": ["yes", "positive"],
        "bad": ["no", "negative", "neutral"],
    }
    DEFAULT = "good"


class Australian(StockMovement):
    DATASET_PATH = "chancefocus/flare-australian"
    CHOICE_DICT = {
        "good": ["yes", "positive"],
        "bad": ["no", "negative", "neutral"],
    }
    DEFAULT = "good"


class ECTSUM(ExtractiveSummarization):
    DATASET_PATH = "chancefocus/flare-ectsum"


class EDTSUM(AbstractiveSummarization):
    DATASET_PATH = "chancefocus/flare-edtsum"

class ESMultiFin(Classification):
    DATASET_PATH = "chancefocus/flare-es-multifin"


class ESEFP(Classification):
    DATASET_PATH = "chancefocus/flare-es-efp"


class ESEFPA(Classification):
    DATASET_PATH = "chancefocus/flare-es-efpa"

class ESTSA(Classification):
    DATASET_PATH = "chancefocus/flare-es-tsa"

class ESFNS(AbstractiveSummarization):
    DATASET_PATH = "chancefocus/flare-es-fns"

class ESFinancees(Classification):
    DATASET_PATH = "chancefocus/flare-es-financees"


class ConvFinQA(QA):
    DATASET_PATH = "chancefocus/flare-convfinqa"

    def reformulate_turn_req(self, req, turn_request, turn):
        if turn == 0:
            return req
        pre_answers = {f"answer{i}": turn_request[i][0] for i in range(turn)}
        if pre_answers:
            req.args = tuple([req.args[0].format(**pre_answers)] + list(req.args[1:]))
        return req


class ZHFinFE(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-fe"


class ZHFinNL(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-nl"


class ZHFinNL2(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-nl2"


class ZHFinNSP(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-nsp"


class ZHFinRE(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-re"


class ZHAFQMC(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-afqmc"


class ZHAstock(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-stocka"


class ZHBQcourse(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-corpus"


class ZHFinEval(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-fineval"


class ZHstock11(Classification):
    DATASET_PATH = "ChanceFocus/flare-zh-stockb"

class ZHFinQA(QA):
    DATASET_PATH = "ChanceFocus/flare-zh-qa"


class ZHFinNA(AbstractiveSummarization):
    DATASET_PATH = "ChanceFocus/flare-zh-na"


class ZH21CCKS(RelationExtraction):
    DATASET_PATH = "ChanceFocus/flare-zh-21ccks"

    def process_results(self, doc, results):
        return {
            "precision": (doc["answer"], results),
            "recall": (doc["answer"], results),
            "f1": (doc["answer"], results),
        }

    def process_string_list(self, string_list):
        processed_list = []

        for item in string_list:
            processed_item = item.strip()
            processed_list.append(processed_item)

        return processed_list

    def process(self, items):
        golds, preds = zip(*items)

        all_golds = []
        all_preds = []

        for gold, pred in zip(golds, preds):
            gold = str(gold).split("\n")
            all_golds.extend(gold)
            pred = self.process_string_list(pred)
            all_preds.extend(pred)
            
        return set(all_golds), set(all_preds)

    def precision(self, items):
        golds, preds = self.process(items)
        gold_len = len(golds)
        count = 0

        for gold_item in golds:
            for pred_item in preds:
                if gold_item & pred_item:
                    count += 1

        print("count:", count)
        prec = count / gold_len
        return prec

    def recall(self, items):
        golds, preds = self.process(items)
        pred_len = len(preds)
        count = 0

        for gold_item in golds:
            for pred_item in preds:
                if gold_item & pred_item:
                    count += 1

        print("count:", count)
        rec = count / pred_len
        return rec

    def cal_f1(self, items):
        prec = self.precision(items)
        rec = self.recall(items)
        if prec + rec == 0.0:
            return 0.0
        return 2 * (prec * rec) / (prec + rec)


class ZH19CCKS(RelationExtraction):
    VERSION = 1
    DATASET_PATH = "ChanceFocus/flare-zh-19ccks"

    def process_results(self, doc, results):
        return {
            "precision": (doc["answer"], results[0]),
            "recall": (doc["answer"], results[0]),
            "f1": (doc["answer"], results[0]),
        }


class ZH20CCKS(ZH19CCKS):
    DATASET_PATH = "ChanceFocus/flare-zh-20ccks"


class ZH22CCKS(ZH19CCKS):
    DATASET_PATH = "ChanceFocus/flare-zh-22ccks"


class ZHNER(NER):
    DATASET_PATH = "ChanceFocus/flare-zh-ner"

    def process_results(self, doc, results):
        text = doc["text"]
        pred = process_zhtext(results[0], text)

        return {"entity_f1": (pred, doc["label"], results[0])}
